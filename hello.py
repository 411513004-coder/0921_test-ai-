def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """計算 BMI 數值（身高公分、體重公斤）"""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi: float) -> str:
    """依據衛福部標準判斷體位區間"""
    if bmi < 18.5:
        return "體重過輕"
    elif bmi < 24:
        return "健康體位 (正常)"
    elif bmi < 27:
        return "過重"
    elif bmi < 30:
        return "輕度肥胖"
    elif bmi < 35:
        return "中度肥胖"
    else:
        return "重度肥胖"


def main():
    print("Hello, World!\n")
    print("=== BMI 計算器 ===")
    try:
        height_input = input("請輸入身高 (cm): ")
        weight_input = input("請輸入體重 (kg): ")
        
        height = float(height_input)
        weight = float(weight_input)
        
        bmi = calculate_bmi(height, weight)
        category = get_bmi_category(bmi)
        
        print(f"\n計算結果：")
        print(f"BMI 指數: {bmi:.2f}")
        print(f"判定結果: {category}")
    except ValueError:
        print("輸入錯誤：請輸入有效的數值。")


if __name__ == "__main__":
    main()
