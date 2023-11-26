import cv2
import sys
from utils.crate_analysis import CrateQualityAnalyzer


if __name__ == "__main__":

    quality_analyzer = CrateQualityAnalyzer("config/setting.yaml")

    if len(sys.argv) != 2:
        print("Usage: python inspect_crate.py <image_path>")

    else:
        image_path = sys.argv[1]
        image = cv2.imread(image_path)

        crate_quality, img_results = quality_analyzer.inspect(image)
        
        print(f"Crate quality: {crate_quality}")        
        
        while cv2.waitKey(1) != 27:
            cv2.imshow("Inspection Results", img_results)
            cv2.imshow("image", image)

