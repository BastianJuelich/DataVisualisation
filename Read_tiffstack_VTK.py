import vtk
import tifffile


def main():
filename = "D:/SparesAMx_V06/Hussein_Versuch/Ti64_Hussein_complete/Hussein/Hussein_800_90.tif"

colors = vtk.vtkNamedColors()

# This is a simple volume rendering 
# uses a vtkFixedPointVolumeRayCastMapper

# Create the standard renderer, render window
# and interactor.
ren1 = vtk.vtkRenderer()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Create the reader for the Tiff-Data (Multi-Image-Tiff)
reader = vtk.vtkTIFFReader()
reader.SetFileName(filename)
reader.SetDataSpacing(1,1,0.3)

# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0)
opacityTransferFunction.AddPoint(20, 0)
opacityTransferFunction.AddPoint(40, 0.15)
opacityTransferFunction.AddPoint(98.26, 0.71)
opacityTransferFunction.AddPoint(253, 0)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0, 0, 0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.1,0.1, 0.1)

# The property describes how the data will look.
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetAmbient(0.2)
volumeProperty.SetDiffuse(1)
volumeProperty.SetSpecular(0)
volumeProperty.SetPower(1)
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
#volumeMapper = vtk.vtkOpenGLGPUColumeRayCastMapper()
colors = vtk.vtkNamedColors()
colors.ResetColors()
#colors.SetColor("BkgColor", [51, 77, 102, 255])
#volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
#volumeProperty.SetIndependentComponents(False)

ren1.AddVolume(volume)
ren1.SetBackground(colors.GetColor3d("Wheat"))
ren1.GetActiveCamera().Azimuth(45)
ren1.GetActiveCamera().Elevation(30)
ren1.ResetCameraClippingRange()
ren1.ResetCamera()
'''
###test box widget to cut through planes###
widget = vtk.vtkBoxWidget()
widget.SetInteractor(iren)
widget.SetPlaceFactor(1.25)

widget.SetInputConnection(reader.GetOutputPort())
widget.PlaceWidget()

def SelectPolygons(object, event):
    # object will be the boxWidget
    global selectActor, planes
    object.GetPlanes(planes)
    selectActor.VisibilityOn()

widget.AddObserver("EndInteractionEvent", SelectPolygons)
widget.PlaceWidget()
#############
'''
renWin.SetSize(600, 600)
renWin.Render()

iren.Start()


def get_program_parameters():
    import argparse
    description = 'Volume rendering of a high potential iron protein.'
    epilogue = '''
    This is a simple volume rendering example that uses a vtkFixedPointVolumeRayCastMapper.
    '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='ironProt.vtk.')
    args = parser.parse_args()
    return args.filename


if __name__ == '__main__':
    main()





# Create the reader for the Tiff-Data (Multi-Image-Tiff)
reader = vtk.vtkTIFFReader()
reader.SetFileName(filename)
reader.SetDataSpacing(1,1,0.3)
reader.Update()

colors = vtk.vtkNamedColors()
colors.SetColor("BkgColor", [51, 77, 102, 255])
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

volumeColor = vtk.vtkColorTransferFunction()
volumeColor.AddRGBPoint(0.0, 0, 0, 0)
volumeColor.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
volumeColor.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
volumeColor.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
volumeColor.AddRGBPoint(255.0, 0.1,0.1, 0.1)

volumeScalarOpacity = vtk.vtkPiecewiseFunction()
volumeScalarOpacity.AddPoint(0, 0.00)
volumeScalarOpacity.AddPoint(50, 1)
volumeScalarOpacity.AddPoint(255, 0)


volumeGradientOpacity = vtk.vtkPiecewiseFunction()
volumeGradientOpacity.AddPoint(10, 0.0)
volumeGradientOpacity.AddPoint(100, 0.5)
volumeGradientOpacity.AddPoint(200, 1.0)



volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(volumeColor)
volumeProperty.SetScalarOpacity(volumeScalarOpacity)

volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.ShadeOn()
volumeProperty.SetAmbient(0.4)
volumeProperty.SetDiffuse(0.6)
volumeProperty.SetSpecular(0.2)

volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

renWin.SetSize(600, 600)
renWin.Render()

iren.Start()
ren.AddViewProp(volume)









luminance = vtk.vtkImageLuminance()
luminance.SetInputConnection(colorVolume.GetImageDataConnection())
append=vtk.vtkImageAppendComponents()
append.AddInputConnection(colorVolume.GetImageDataConnection())
append.AddInputConnection(luminance.GetOutputPort())
append.Update()
colorVolume.SetAndObserveImageData(append.GetOutput())