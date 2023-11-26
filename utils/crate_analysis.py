import cv2
import numpy as np
import yaml
from skimage.metrics import structural_similarity as ssim

class CrateQualityAnalyzer():
    """ CrateQualityAnalyzer Class
    Analyzes the quality of a crate
    """
    
    # Health stats
    HEALTH_OK = "OK"
    HEALTH_BAD = "FAULTY"

    
    def __init__(self, path_settings):
        """ 
        CrateQualityAnalyzer Constructor 

        Args:
            path_settings (str): Path to the settings file
        """
        self.settings = self.load_settings(path_settings)
        
        self.ok_case_template = cv2.imread(self.settings["TEMPLATE"]["IMAGE"], 0)
        self.ok_case_template = cv2.resize(self.ok_case_template, (self.settings["TEMPLATE"]["WIDTH"], self.settings["TEMPLATE"]["HEIGHT"]))
        
        self.fault_icon = cv2.imread("assets/fault_icon.jpg")
        self.fault_icon = cv2.resize(self.fault_icon, (self.settings["TEMPLATE"]["WIDTH"], self.settings["TEMPLATE"]["HEIGHT"]))
        
    def load_settings(self, path_settings):
        """
        Load settings from a YAML file

        Args:
            path_settings (str): Path to the settings file

        Returns:
            dict: Settings loaded from the file

        Raises:
            FileNotFoundError: If the settings file is not found
        """       
        try:
            with open(path_settings, "r") as f:
                settings = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError as err:
            raise FileNotFoundError("Settings file not found") from err

        return settings


    def preprocess(self, image):       
        """ 
        Preprocess image for analysis 

        Args:
            image (np.array): Input image

        Returns:
            np.array: Preprocessed image
        """

        proc_img = image.copy()
        proc_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return proc_img
    
    def apply_feather(self, rectangle):
        """ 
        Apply feather to rectangle 

        Args:
            rectangle (tuple): A tuple containing the coordinates of the rectangle (x, y, width, height)

        Returns:
            tuple: A tuple containing the coordinates of the rectangle after applying feather
        """
        x, y, w, h = rectangle
        feather_x = int(self.settings["FEATHER"]["X"] * w)
        feather_y = int(self.settings["FEATHER"]["Y"] * h)
        return x + feather_x, y + feather_y, w - 2 * feather_x, h - 2 * feather_y
        
        
    def get_slots(self, gray_image):
        """
        Get the slots in the crate based on the provided gray image.

        Args:
            gray_image (numpy.ndarray): The gray image of the crate.

        Returns:
            list: A list of tuples representing the slots in the crate. Each tuple contains the four corner points of a slot.
        """
        
        slots = []
        img = gray_image.copy()
        
        edges = cv2.Canny(img, self.settings["CANNY_THRESHOLD"], 255)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        all_contours = np.concatenate(contours)
        
        crate_bb = cv2.boundingRect(all_contours)
        crate_x, crate_y, crate_w, crate_h = self.apply_feather(crate_bb)
        cell_width = crate_w // self.settings["CRATE"]["COLS"]
        cell_height = crate_h // self.settings["CRATE"]["ROWS"]
        
        for x in range(crate_x, crate_x + crate_w - cell_width + 1, cell_width):
            for y in range(crate_y, crate_y + crate_h - cell_height + 1, cell_height):
                pt1 = (x, y)
                pt2 = (x + cell_width, y)
                pt3 = (x + cell_width, y + cell_height)
                pt4 = (x, y + cell_height)
                slots.append((pt1, pt2, pt3, pt4))
                
        return slots
                
    def annotate_quality_results(self, image, quality_report):
            """ Annotate image with quality results
            
            Args:
                image (numpy.ndarray): The input image to be annotated.
                quality_report (dict): A dictionary containing the quality report for each slot in the image.
            
            Returns:
                numpy.ndarray: The annotated image.
            """
            
            img = image.copy()
            overlay_mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
            
            
            crate_quality = self.assess_crate_health(quality_report)

            
            for slot_id, (slot, health) in quality_report.items():
                center = (int((slot[0][0] + slot[2][0]) / 2), int((slot[0][1] + slot[2][1]) / 2))      
                if health == self.HEALTH_BAD and crate_quality == self.HEALTH_BAD:
                    icon_mapped = cv2.resize(self.fault_icon, (slot[2][0] - slot[0][0], slot[2][1] - slot[0][1]))
                    overlay_mask[slot[0][1]:slot[2][1], slot[0][0]:slot[2][0]] = icon_mapped
                elif health == self.HEALTH_OK and crate_quality == self.HEALTH_OK:
                    cv2.drawMarker(overlay_mask, center, (0, 255, 0), cv2.MARKER_CROSS, 20, 1)
                    
            if(crate_quality == self.HEALTH_BAD):
                img = cv2.addWeighted(overlay_mask, 0.5, img, 1 - 0.5, 0, img)
                cv2.putText(img, "BAD !", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)        
            else:
                img = cv2.addWeighted(overlay_mask, 0.5, img, 1 - 0.5, 0, img)
                cv2.putText(img, "OK !", ( 10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            return img

    def detect_circle(self, cropped_img):
        """
        Detects the largest circle in the given cropped image using the Hough Circle Transform.

        Args:
            cropped_img (numpy.ndarray): The cropped image to analyze.

        Returns:
            tuple or None: A tuple containing the (x, y, radius) coordinates of the largest circle found in the image,
            or None if no circle is found.
        """
        img = cropped_img.copy()
        img = cv2.threshold(img, self.settings["HOUGHCIRCLES"]["THRESHOLD"], 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        img = cv2.medianBlur(img, 5)
        
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=self.settings["HOUGHCIRCLES"]["PARAM1"], param2=self.settings["HOUGHCIRCLES"]["PARAM2"], minRadius=self.settings["HOUGHCIRCLES"]["MIN_RADIUS"], maxRadius=self.settings["HOUGHCIRCLES"]["MAX_RADIUS"])
        largest_circle = None
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0]:
                if largest_circle is None or circle[2] > largest_circle[2]:
                    largest_circle = circle
        
        return largest_circle
        
        
    def assess_slot_health(self, slot, image):
            """ 
            Assess the health of a slot 
            
            Parameters:
            - slot (list): The coordinates of the slot in the image.
            - image (numpy.ndarray): The input image containing the slot.
            
            Returns:
            - str: The health status of the slot. Possible values are "OK" or "BAD".
            """
            
            mask = np.zeros_like(image)
            cv2.fillPoly(mask, np.array([list(slot)]), (255,255,255))
            slot_img = cv2.bitwise_and(image, mask)
            
            slot_img_cropped = slot_img[slot[0][1]:slot[2][1], slot[0][0]:slot[2][0]]
            slot_img_cropped = cv2.resize(slot_img_cropped, (self.ok_case_template.shape[1], self.ok_case_template.shape[0]))        
            

            possible_bottle_mouth = self.detect_circle(slot_img_cropped)
            template_bottle_mouth = self.detect_circle(self.ok_case_template)
            
            if possible_bottle_mouth is not None and template_bottle_mouth is not None:
                percentage_error =  100 * abs(int(possible_bottle_mouth[2]) - int(template_bottle_mouth[2])) / (0.5 * (abs(int(template_bottle_mouth[2]))  + abs(int(possible_bottle_mouth[2]))))
                if percentage_error <= self.settings["MATCHING"]["ERROR_THRESHOLD"]:
                    return self.HEALTH_OK
            
            return self.HEALTH_BAD
    
        
    def assess_crate_health(self, quality_report):
            """ Check if crate is good via slot health
            
            Args:
                quality_report (dict): A dictionary containing the health status of each slot in the crate.
            
            Returns:
                str: The health status of the crate. Possible values are 'BAD' or 'OK'.
            """
            
            for _ , health in quality_report.values():
                if health == self.HEALTH_BAD:
                    return self.HEALTH_BAD
            
            return self.HEALTH_OK

    def inspect(self, image): 
            """ 
            Inspect crate for quality 
            
            Args:
                image (numpy.ndarray): The input image of the crate.
            
            Returns:
                tuple: A tuple containing the crate quality score and the annotated image.
            """
            quality_report = {}
            org_img = image.copy()
            org_img = cv2.resize(org_img,
             (self.settings["IMAGE"]["WIDTH"],
              self.settings["IMAGE"]["HEIGHT"]))     
            
            # preprocess image to grayscale
            processed_img  =  self.preprocess(org_img)

            # get slots [(p1, p2, p3, p4)]
            slots = self.get_slots(processed_img)
            
            for slot_id, slot in enumerate(slots):
                slot_quality = self.assess_slot_health(slot,processed_img)
                quality_report[slot_id] = [slot, slot_quality]

            crate_quality = self.assess_crate_health(quality_report)

            annotated_img = self.annotate_quality_results(org_img, quality_report)
            

            return crate_quality, annotated_img

        