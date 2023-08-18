import os
import slicer

#目前只能转换10个以内的文件

stl_path = r"E:\bigorgs\Coronary\3D\test\stl"
image_path = r"E:\bigorgs\Coronary\3D\test\temp"
out_path = r"E:\bigorgs\Coronary\3D\test\output"

patients = os.listdir(stl_path)
print(patients)

for patient in patients:
    stl_files = os.listdir(stl_path)
    output_file_path = os.path.join(out_path, patient)
    os.makedirs(output_file_path, exist_ok=True)
    reference_volume_path = os.path.join(image_path, patient[0]+".nii.gz")
    referenceVolumeNode = slicer.util.loadVolume(reference_volume_path)
    for stl_file in stl_files:
        stl_file_name = os.path.join(stl_path, stl_file)
        output_file_name = os.path.join(output_file_path, stl_file[0] + ".nii.gz")
        segmentationNode = slicer.util.loadSegmentation(stl_file_name)
        outputLabelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode')
        slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode, outputLabelmapVolumeNode,
                                                                                 referenceVolumeNode)
        slicer.util.saveNode(outputLabelmapVolumeNode, output_file_name)
        slicer.mrmlScene.Clear(0)