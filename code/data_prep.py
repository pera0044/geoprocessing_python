import sys
import os

def main():
    global arcpy

    if len(sys.argv) !=4:
        print('Usage: data_prep.py <in_gdbs_base_folder> <out_gdb> <out_feature_dataset>')
        sys.exit()

    in_gdbs_base_folder = sys.argv[1]
    out_gdb = sys.argv[2]
    out_feature_dataset = sys.argv[3]

    if not os.path.exists(in_gdbs_base_folder):
        print(f'{in_gdbs_base_folder} folder does not exist')
        sys.exit()
    
    elif not os.path.exists(os.path.dirname(out_gdb)):
        print(f'{os.path.dirname(out_gdb)} folder does not exist')
        sys.exit()
    
    import arcpy

    gdbs_to_fds(in_gdbs_base_folder, out_gdb, out_feature_dataset)    


def gdbs_to_fds(in_gdbs_base_folder, out_gdb, out_feature_dataset):
    
    arcpy.env.overwriteOutput = True

    arcpy.env.workspace = in_gdbs_base_folder

    # Create file geodatabase
    path_out_gdb = arcpy.management.CreateFileGDB(out_folder_path = os.path.dirname(out_gdb), out_name = os.path.basename(out_gdb), out_version = "CURRENT")[0]
    
    # Create Feature Dataset
    workspaces = arcpy.ListWorkspaces()
    arcpy.env.workspace = os.path.join(in_gdbs_base_folder, workspaces[0])
    feature_classes = arcpy.ListFeatureClasses("*")
    desc = arcpy.Describe(feature_classes[0])
    sr = desc.spatialReference
    path_out_feature_dataset = arcpy.management.CreateFeatureDataset(out_dataset_path = path_out_gdb, out_name = out_feature_dataset, spatial_reference = sr)[0]

    # Transfer feature classes from other geodatabases to the new feature dataset
    for dirpath, __, __ in os.walk(in_gdbs_base_folder, topdown = True):
        arcpy.env.workspace = dirpath
        in_feature_classes = arcpy.ListFeatureClasses("*")
        for feature in in_feature_classes:
            path_in_feature_class = os.path.join(dirpath, feature)
            path_transfered_fc = arcpy.conversion.FeatureClassToFeatureClass(in_features = path_in_feature_class, out_path = path_out_feature_dataset, out_name = feature)[0]
    
    return path_out_feature_dataset


if __name__ == '__main__':
    main()