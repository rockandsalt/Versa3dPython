import vtk
import numpy as np
import math
from vtk.util.numpy_support import vtk_to_numpy
from collections import namedtuple
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

from abc import ABC, abstractmethod

class GenericSlicer(ABC):        
    @abstractmethod
    def update_printer(self, setting):
        raise NotImplementedError

    @abstractmethod
    def update_printhead(self, setting):
        raise NotImplementedError
    
    @abstractmethod
    def update_param(self, setting):
        raise NotImplementedError

    @abstractmethod
    def slice_object(self, object):
        pass

class FullBlackSlicer(GenericSlicer):
    def __init__(self):
        self._resolution = np.array([50, 50], dtype=int)
        self._layer_thickness = 0.1
    
    def update_printhead(self, setting):
        if not 'dpi' in setting:
            raise ValueError

        if np.any(setting['dpi'].value != self._resolution):
            self._resolution = setting['dpi']
            return True
        return False
    
    def update_param(self, setting):
        if not 'layer_thickness' in setting:
            raise ValueError

        if setting['layer_thickness'].value != self._layer_thickness:
            self._resolution = setting['layer_thickness'].value
            return True
        return False
    
    def update_printer(self, setting):
        return False
    
    @staticmethod
    def compute_spacing(layer_thickness, resolution):
        spacing = np.zeros(3, dtype=float)
        spacing[0:2] = 25.4/resolution
        spacing[2] = np.min(layer_thickness)
        return spacing
    
    @staticmethod
    def compute_dim(bounds, spacing):
        return np.ceil(( bounds[1::2] - bounds[0::2] ) / spacing).astype(int)
    
    def update_info(self, input_src, outInfo):
        spacing = self.compute_spacing(self._layer_thickness, self._resolution)
        bounds = np.array(input_src.GetBounds())
        img_dim = self.compute_dim(bounds, spacing)
        outInfo.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(),
            (0, img_dim[0]-1, 0, img_dim[1]-1, 0, img_dim[2]-1), 6)
    
    def slice_object(self, input_src):
        bounds = np.array(input_src.GetBounds())
        spacing = self.compute_spacing(self._layer_thickness, self._resolution)
        img_dim = self.compute_dim(bounds, spacing)
        origin = bounds[0::2]

        background_img = vtk.vtkImageData()
        background_img.SetSpacing(spacing)
        background_img.SetDimensions(img_dim)
        background_img.SetOrigin(origin)
        background_img.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
        background_img.GetPointData().GetScalars().Fill(0)

        poly_sten = vtk.vtkPolyDataToImageStencil()
        poly_sten.SetInputData(input_src)
        poly_sten.SetOutputOrigin(origin)
        poly_sten.SetOutputSpacing(spacing)
        poly_sten.SetOutputWholeExtent(background_img.GetExtent())
        poly_sten.Update()

        stencil = vtk.vtkImageStencil()
        stencil.SetInputData(background_img)
        stencil.SetStencilConnection(poly_sten.GetOutputPort())
        stencil.SetBackgroundValue(255)
        stencil.ReverseStencilOff()
        stencil.Update()
        return stencil.GetOutput()

class VoxelSlicer(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=1, inputType = 'vtkPolyData', 
            nOutputPorts=1, outputType='vtkImageData')
        
        self.slicer = None
    
    def set_settings(self, printer, printhead, print_param):
        self.set_print_parameter(print_param)
        self.set_printer(printer)
        self.set_printhead(printhead)
    
    def set_printer(self, setting):
        if self.slicer.update_printer(setting):
            self.Modified()
    
    def set_printhead(self, setting):
        if self.slicer.update_printhead(setting):
            self.Modified()
    
    def set_print_parameter(self, setting):
        if setting['fill_pattern'].value == 0:
            self.slicer = FullBlackSlicer()
        else:
            raise ValueError
        
        if self.slicer.update_param(setting):
            self.Modified()
    
    def RequestInformation(self, request, inInfo, outInfo):
        input_src = vtk.vtkPolyData.GetData(inInfo[0])
        info = outInfo.GetInformationObject(0)
        self.slicer.update_info(input_src, info)
        return 1

    def RequestData(self, request, inInfo, outInfo):
        input_src = vtk.vtkPolyData.GetData(inInfo[0])
        output = vtk.vtkImageData.GetData(outInfo)
        output.ShallowCopy(self.slicer.slice_object(input_src))
        return 1