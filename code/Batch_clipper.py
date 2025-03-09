import sys
import os


def main():
    global arcpy

    if len(sys.argv) !=4:
        print("Usage:  batch_clipper.py <InWorkspace> <ClipWorkspace> <OutputWorkspace>")
        sys.exit()

    in_workspace = sys.argv[1]
    clip_workspace =sys.argv[2]
    output_workspace = sys.argv[3]

    if not os.path.exists(in_workspace):
        print(f'{in_workspace} path does not exist')
        sys.exit()

    elif not os.path.exists(clip_workspace):
        print(f'{clip_workspace} path does not exist')
        sys.exit()

    elif not os.path.exists(output_workspace):
        print(f'{output_workspace} path does not exist')
        sys.exit()
    
    import arcpy

    clip_featureclasses(in_workspace, clip_workspace, output_workspace)  

def clip_featureclasses(in_workspace, clip_workspace, output_workspace):

    arcpy.env.overwriteOutput = True

    list_feature_classes = []
    arcpy.env.workspace = in_workspace
    in_feature_classes = arcpy.ListFeatureClasses("*")
    for feature in in_feature_classes:
        list_feature_classes.append(os.path.join(os.path.abspath(in_workspace), feature))

    list_feature_classes_clip = []
    arcpy.env.workspace = clip_workspace
    clip_feature_classes = arcpy.ListFeatureClasses("*")
    for feature in clip_feature_classes:
        list_feature_classes_clip.append(os.path.join(os.path.abspath(clip_workspace), feature))
            
    for in_feature in list_feature_classes:
        for clip_feature in list_feature_classes_clip:
            in_feature_name = os.path.split(in_feature)[1]
            clip_feature_name = os.path.split(clip_feature)[1]
            output_name = f"{clip_feature_name.rstrip('.shp')}_{in_feature_name}"
            path_output_workspace = os.path.join(os.path.abspath(output_workspace), output_name)
            arcpy.Clip_analysis(in_feature, clip_feature, path_output_workspace)
        
if __name__ == "__main__":
    main()