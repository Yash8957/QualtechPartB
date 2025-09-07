import os
import json
from collections import defaultdict
import io
import time

try:
    import requests
    from ultralytics import YOLO

    # All application logic is now placed inside this 'try' block
    # to ensure it only runs if the imports are successful.
    
    # This script provides a solution for an Intelligent Video Analysis system.
    # It uses the ultralytics library to directly analyze images from URLs sourced
    # dynamically from the Unsplash API, without requiring a local dataset download.
    
    def fetch_image_urls_from_unsplash(query, count=5):
        """
        Fetches image URLs from the Unsplash API based on a search query.
    
        Args:
            query (str): The search term to find relevant images.
            count (int): The number of image URLs to fetch.
    
        Returns:
            list: A list of image URLs. Returns an empty list on failure.
        """
        access_key = "YOUR_UNSPLASH_ACCESS_KEY"  # <-- REPLACE WITH YOUR ACCESS KEY
        if access_key == "YOUR_UNSPLASH_ACCESS_KEY":
            print("Error: Please replace 'YOUR_UNSPLASH_ACCESS_KEY' with your actual Unsplash API key.")
            return []
    
        url = f"https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {access_key}"}
        params = {"query": query, "per_page": count}
    
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            image_urls = [result['urls']['regular'] for result in data['results']]
            return image_urls
        except requests.exceptions.RequestException as e:
            print(f"Error fetching images from Unsplash for query '{query}': {e}")
            return []
    
    def analyze_video_background(model, image_urls, declared_data):
        """
        Analyzes a sequence of images (simulating a video) to classify the environment,
        detect objects, and compare against declared data.
    
        Args:
            model (YOLO): The pre-trained YOLO model instance.
            image_urls (list): A list of URLs for the video frames.
            declared_data (dict): The declared environment and assets.
    
        Returns:
            dict: A structured report with analysis results and fraud flags.
        """
        print(f"\nAnalyzing video background with {len(image_urls)} frames...")
    
        # Define rules for environment classification
        env_rules = {
            "Home": ["bed", "sofa", "tv", "refrigerator", "microwave", "chair", "dining table"],
            "Office": ["desk", "computer", "whiteboard", "chair", "meeting table"],
            "Shop": ["shelf", "counter", "bottled products", "packaged boxes", "refrigerator"]
        }
        
        all_detected_items = defaultdict(list)
        all_detected_counts = defaultdict(int)
        
        # Analyze each image to accumulate object data
        for i, image_url in enumerate(image_urls):
            print(f"  Processing frame {i+1}/{len(image_urls)}: {image_url}")
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                image_data = io.BytesIO(response.content)
                results = model.predict(source=image_data, conf=0.5, verbose=False)
            except requests.exceptions.RequestException as e:
                print(f"  Error fetching image from URL {image_url}: {e}")
                continue
    
            if results and results[0].boxes:
                for box in results[0].boxes:
                    class_id = int(box.cls)
                    confidence = float(box.conf)
                    item_name = model.names[class_id]
                    
                    all_detected_items[item_name].append(confidence)
                    all_detected_counts[item_name] += 1
    
        # Classify environment based on detected objects
        detected_environment = "Uncategorized"
        environment_confidence = 0.0
        
        for env, items in env_rules.items():
            common_items = [item for item in items if item in all_detected_counts]
            if common_items:
                detected_environment = env
                total_confidence = sum(
                    sum(all_detected_items[item]) for item in common_items
                )
                total_count = sum(all_detected_counts[item] for item in common_items)
                if total_count > 0:
                    environment_confidence = round(total_confidence / total_count, 2)
                break
    
        # Compare against declared data and identify mismatches
        mismatches = []
        risk_flag = "Pass"
        
        declared_env = declared_data.get("environment")
        declared_assets = declared_data.get("assets", {})
        
        # Mismatch 1: Environment type
        if declared_env and declared_env.lower() != detected_environment.lower():
            mismatches.append(f"Declared environment '{declared_env}' does not match detected environment '{detected_environment}'")
            risk_flag = "Review Required"
        
        # Mismatch 2: Asset counts
        for asset, declared_count in declared_assets.items():
            detected_count = all_detected_counts.get(asset, 0)
            if declared_count != detected_count:
                mismatches.append(f"Declared '{asset}: {declared_count}' but detected '{asset}: {detected_count}'")
                risk_flag = "Review Required"
        
        # Generate final report
        final_report = {
            "declared_data": declared_data,
            "analysis_results": {
                "detected_environment": detected_environment,
                "environment_confidence": environment_confidence,
                "detected_objects": [
                    {
                        "item": item.title(),
                        "count": all_detected_counts[item],
                        "avg_confidence": round(sum(confidences) / len(confidences), 2)
                    }
                    for item, confidences in all_detected_items.items()
                ]
            },
            "mismatch_highlight": mismatches,
            "risk_flag": risk_flag
        }
    
        return final_report
    
    def generate_report(report_data, output_file):
        """
        Generates a structured report in JSON format.
        """
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=4)
        print(f"Analysis report saved to {output_file}")
    
    def main():
        """
        Main function to run the intelligent background verification.
        """
        print("Initializing Intelligent Background Verification solution.")
        
        try:
            model = YOLO('yolov8n.pt')
            print("Pre-trained YOLOv8n model loaded successfully.")
    
            # --- Use Case A: Declared "Home", Detected "Shop" ---
            declared_data_a = {
                "environment": "Home",
                "assets": {"refrigerator": 2, "sofa": 1}
            }
            shop_image_urls = fetch_image_urls_from_unsplash("supermarket shelves, retail store", count=3)
            report_a = analyze_video_background(model, shop_image_urls, declared_data_a)
            
            generate_report([report_a], "verification_report_A.json")
            print("\n--- Verification Report A (Declared 'Home', Detected 'Shop') ---")
            print(json.dumps(report_a, indent=4))
    
            # --- Use Case B: Declared "Shop", Detected "Home" ---
            declared_data_b = {
                "environment": "Shop",
                "assets": {"refrigerator": 1, "counter": 1}
            }
            home_image_urls = fetch_image_urls_from_unsplash("living room, home kitchen", count=3)
            report_b = analyze_video_background(model, home_image_urls, declared_data_b)
    
            generate_report([report_b], "verification_report_B.json")
            print("\n--- Verification Report B (Declared 'Shop', Detected 'Home') ---")
            print(json.dumps(report_b, indent=4))
    
            # --- Use Case C: Declared "Home", Detected "Home" (Pass) ---
            declared_data_c = {
                "environment": "Home",
                "assets": {"sofa": 1, "chair": 2}
            }
            home_image_urls_c = fetch_image_urls_from_unsplash("home living room, sofa, kitchen", count=3)
            report_c = analyze_video_background(model, home_image_urls_c, declared_data_c)
            
            generate_report([report_c], "verification_report_C.json")
            print("\n--- Verification Report C (Declared 'Home', Detected 'Home') ---")
            print(json.dumps(report_c, indent=4))
    
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred during an HTTP request: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    if __name__ == "__main__":
        main()

except ImportError as e:
    # This block is only executed if the imports fail.
    print(f"Error: A required library was not found. Please install the necessary packages.")
    print(f"Specifically, the following import failed: {e}")
    print(f"You can install them by running 'pip install ultralytics requests'.")
    exit()
