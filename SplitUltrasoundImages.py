from PIL import Image
import os

def copyfile(input_file, output_file, c):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        processed_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 9 and parts[0].isdigit():  # 確保格式正確
                label = parts[0]
                coords = list(map(float, parts[1:]))

                # 處理 x 值 (索引為 0, 2, 4, 6)
                if c == 0:
                    for i in range(0, len(coords), 2):
                        coords[i] = (coords[i] * 420) / 214
                else:
                    for i in range(0, len(coords), 2):
                        coords[i] = (coords[i] * 420 + 20) / 206

                # 重建處理後的標記行
                processed_line = f"{label} " + " ".join(f"{coord:.6f}" for coord in coords)
                processed_lines.append(processed_line)

        # 寫入結果到輸出檔案
        with open(output_file, 'w') as outfile:
            outfile.write("\n".join(processed_lines))

    except Exception as e:
        print(f"發生錯誤: {e}")

def split_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    available_txts = {txt for txt in os.listdir(input_folder) if txt.endswith('.txt')}

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)
            width, height = image.size

            # 分割圖片，原圖片大小為420*310
            # 左側黑白大小變為 214*310
            # 右側彩色大小變為 206*310
            left_half = image.crop((0, 0, 214, height))
            right_half = image.crop((214, 0, width, height))

            # 儲存分割後的圖片
            base_name, ext = os.path.splitext(filename)
            left_half.save(os.path.join(output_folder, f"{base_name}_BW{ext}"))
            right_half.save(os.path.join(output_folder, f"{base_name}_COLOR{ext}"))

            #複製文件(標記代號 x1 y1 x2 y2 x3 y3 x4 y4)比例
            source_file = base_name + ".txt"
            if source_file in available_txts:
                source_file = os.path.join(input_folder, source_file)

                destination_file = os.path.join(output_folder, f"{base_name}_BW.txt")
                copyfile(source_file, destination_file, 0)

                destination_file = os.path.join(output_folder, f"{base_name}_COLOR.txt")
                copyfile(source_file, destination_file, 1)

    print("分割完成")

split_images('胸骨旁短軸\\two_piece', '胸骨旁短軸\\after')
