from PIL import Image
import os

input_folder = "./"
output_sizes = [(64, 64)]

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        png_path = os.path.join(input_folder, filename)
        ico_path = os.path.join(input_folder, os.path.splitext(filename)[0] + ".ico")

        try:
            img = Image.open(png_path)

            # 强制转换为 RGBA（保留透明度），避免 P 模式
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")

            # 检查是否完全透明（避免生成空图标）
            alpha = img.getchannel("A") if img.mode == "RGBA" else None
            if alpha and not alpha.getextrema()[1]:  # 最大值为 0 → 全透明
                print(f"⚠️ 跳过空白图像: {filename}")
                continue

            # 生成多个尺寸图层
            resized_images = [img.resize(size, Image.LANCZOS) for size in output_sizes]

            # 保存为 ICO，包含多个图层
            resized_images[0].save(ico_path, format='ICO', sizes=output_sizes)
            print(f"✅ 成功转换: {filename} → {os.path.basename(ico_path)}")
        except Exception as e:
            print(f"❌ 转换失败: {filename}，错误信息: {e}")
