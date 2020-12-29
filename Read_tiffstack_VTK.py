import vtk
import tifffile

filename = "filepath/filename.tif"

colors = vtk.vtkNamedColors()

# This is a simple volume rendering 
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
# Values from slicer app
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0)
opacityTransferFunction.AddPoint(20, 0)
opacityTransferFunction.AddPoint(40, 0.15)
opacityTransferFunction.AddPoint(98.26, 0.71)
opacityTransferFunction.AddPoint(253, 0)

# Create transfer mapping scalar value to color.
# How to get Image color for 3d ?
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
###test box widget to cut through planes### just for testing
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

