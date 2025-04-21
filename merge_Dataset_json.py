import json
import os

def merge_coco_datasets(datasets, output_path):
    """
    合併多個 COCO 格式的 JSON 檔案。

    Args:
        datasets: 一個包含字典的列表，每個字典代表一個 dataset，包含以下鍵：
            json_path: JSON 檔案的路徑。
            folder: 圖片所在的資料夾路徑。
        output_path: 輸出 JSON 檔案的路徑。
    """

    merged = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    image_id_offset = 0
    annotation_id_offset = 0

    for i, dataset in enumerate(datasets):
        json_path = dataset["json_path"]
        folder = dataset["folder"]

        with open(json_path, 'r') as f:
            coco = json.load(f)

        # 處理 categories，只取第一個 dataset 的 categories
        if i == 0:
            merged["categories"] = coco["categories"]
        else:
            # 檢查 categories 是否相同 (可選)
            if coco["categories"] != merged["categories"]:
                print(f"警告：{json_path} 的 categories 與第一個 dataset 不同，請確認。")

        # 修改路徑和 ID
        for img in coco["images"]:
            img["file_name"] = os.path.join(folder, img["file_name"])
            img["id"] += image_id_offset
            merged["images"].append(img)

        for ann in coco["annotations"]:
            ann["id"] += annotation_id_offset
            ann["image_id"] += image_id_offset
            merged["annotations"].append(ann)

        # 更新 offset
        image_id_offset = max(img["id"] for img in merged["images"]) + 1 if merged["images"] else 0
        annotation_id_offset = max(ann["id"] for ann in merged["annotations"]) + 1 if merged["annotations"] else 0

    with open(output_path, 'w') as f:
        json.dump(merged, f, indent=4)

    print(f"✅ 合併完成，輸出：{output_path}")


# 範例用法
datasets = [
    {
        "json_path": r'D:\Code\RT-DETR-test\MOBDRONE_split_dataset\annotations\val.json',
        "folder": r'D:\Code\RT-DETR-test\MOBDRONE_split_dataset\val\images'
    },
    {
        "json_path": r'D:\Code\RT-DETR-test\raw_dataset\WiSARD_VIS-4\valid\_annotations.coco.json',
        "folder": r'D:\Code\RT-DETR-test\raw_dataset\WiSARD_VIS-4\valid'
    },
    {
        "json_path": r'D:\Code\RT-DETR-test\raw_dataset\Person_detection\valid\_annotations.coco.json',  # 替換成你的路徑
        "folder": r'D:\Code\RT-DETR-test\raw_dataset\Person_detection\valid'  # 替換成你的路徑
    }
]

merge_coco_datasets(
    datasets=datasets,
    output_path=r'D:\Code\RT-DETR-test\test\valid.json'
)