#include "gtest/gtest.h"
#include "vtkNew.h"
#include <vtkWeakPointer.h>
#include <vtkImageData.h>
#include <vtkPointData.h>
#include <vtkDataArray.h>
#include "bmpwriter.h"

using namespace std;

class bmpwriterTest : public ::testing::Test
{
    protected:
        void SetUp() override {
            black_img->SetSpacing(0.04,0.04,0.01);
            black_img->SetDimensions(360,360,1);
            black_img->AllocateScalars(VTK_FLOAT, 1);
            vtkWeakPointer<vtkPointData> vtk_point_data = black_img->GetPointData();
            vtkWeakPointer<vtkDataArray> array = vtk_point_data->GetScalars();
            array->Fill(0);

            grey_img->SetSpacing(0.04,0.04,0.01);
            grey_img->SetDimensions(360,360,1);
            grey_img->AllocateScalars(VTK_FLOAT, 1);
            vtkWeakPointer<vtkPointData> g_vtk_point_data = grey_img->GetPointData();
            vtkWeakPointer<vtkDataArray> g_array = g_vtk_point_data->GetScalars();
            g_array->Fill(255*0.5);
        }

        vtkNew<vtkImageData> black_img;
        vtkNew<vtkImageData> grey_img;
};

TEST_F(bmpwriterTest, print_black)
{
    char path[] = "./test/testOutput/bmpwriter_output/image.bmp"; 
    unique_ptr<bmpwriter> writer = make_unique<bmpwriter>(black_img);
    writer->write_to_file(path);
}

TEST_F(bmpwriterTest, print_grey)
{
    char path[] = "./test/testOutput/bmpwriter_output/image_g.bmp"; 
    unique_ptr<bmpwriter> writer = make_unique<bmpwriter>(grey_img);
    writer->write_to_file(path);
}

TEST_F(bmpwriterTest, split_print_black)
{
    char path[] = "./test/testOutput/bmpwriter_output/image_split_b.bmp"; 
    unique_ptr<bmpwriter> writer = make_unique<bmpwriter>(black_img);
    writer->split_print(path,10,150);
}

TEST_F(bmpwriterTest, split_print_grey)
{
    char path[] = "./test/testOutput/bmpwriter_output/image_split_g.bmp"; 
    unique_ptr<bmpwriter> writer = make_unique<bmpwriter>(grey_img);
    writer->split_print(path,10,150);
}