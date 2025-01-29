import random
import pandas as pd

from pathlib import Path
from PIL import Image, ImageOps

import streamlit as st


def change_page():
    st.session_state["page_control"] += 1


def a(path):
    # with open("./data/result.csv", mode="a", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     writer.writerow([
    #         st.session_state["Name"],
    #         path.split("/")[-1],
    #         0 if path.split("/")[-2] == "input" else 1
    #     ])
    st.session_state.df = pd.concat([
        st.session_state.df,
        pd.DataFrame({
            "User": [st.session_state["Name"]],
            "Image_ID": [path.split("/")[-1]],
            "Select": [0 if path.split("/")[-2] == "input" else 1]
        })
    ])
    st.session_state.current_index += 1
    # print(path, "左")


def b(path):
    # with open("./data/result.csv", mode="a", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     writer.writerow([
    #         st.session_state["Name"],
    #         path.split("/")[-1],
    #         0 if path.split("/")[-2] == "input" else 1
    #     ])
    st.session_state.df = pd.concat([
        st.session_state.df,
        pd.DataFrame({
            "User": [st.session_state["Name"]],
            "Image_ID": [path.split("/")[-1]],
            "Select": [0 if path.split("/")[-2] == "input" else 1]
        })
    ])
    st.session_state.current_index += 1
    # print(path, "右")


def first_page():
    st.title("画像選択アンケート")
    name = st.text_input("名前を入力してください。", max_chars=50)
    st.session_state["Name"] = name

    st.button("Start", on_click=change_page)


def show_image(input_list, output_list):
    if st.session_state.current_index == len(input_list) - 1:
        change_page()

    st.title("画像選択アンケート")
    st.write("美味しそうに見える方の画像を選択してください。")

    current_index = st.session_state.current_index

    image1_path = input_list[current_index]
    image2_path = output_list[current_index]

    if random.random() < 0.5:
        image1_path, image2_path = image2_path, image1_path

    # Load Image
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Resize
    image1 = ImageOps.expand(image1.resize((512, 512)), border=1, fill="black")
    image2 = ImageOps.expand(image2.resize((512, 512)), border=1, fill="black")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image1)
        st.button("選択", key="left", on_click=a, args=(str(image1_path), ))

    with col2:
        st.image(image2)
        st.button("選択", key="right", on_click=b, args=(str(image2_path), ))


def last_page():    # 3ページ目
    st.title("画像選択アンケート")
    st.write("アンケートは終了です。ご協力ありがとうございました。")
    st.write("以下のボタンをクリックすると、結果がダウンロードされます。")

    # Backup CSV file
    # now = datetime.datetime.now()
    # path = "./data/backup_{}.csv".format(now.strftime('%Y%m%d_%H-%M'))
    # shutil.copy("./data/result.csv", path)

    df = st.session_state.df
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="result.csv",
        mime="text/csv"
    )


def main():
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #007bff; /* ボタンの色を青に設定 */
            color: white;   /* 文字色を白に設定 */

            display: block;
            margin: 0 auto;
            width: 200px;   /* サイズ */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # 画像ディレクトリのパス
    input_dir = Path("./images/input")
    output_dir = Path("./images/output")

    # 画像ファイルのリストを取得
    input_paths = [str(p) for p in input_dir.glob("**/*") if p.is_file()]
    output_paths = [str(p) for p in output_dir.glob("**/*") if p.is_file()]

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame({
            "User": [],
            "Image_ID": [],
            "Select": []
        })

    # writer.writerow(["User", "Image_ID", "Select"])  # Select -> input:0, output:1

    if ("page_control" in st.session_state and st.session_state["page_control"] == 1):
        show_image(input_paths, output_paths)

    elif ("page_control" in st.session_state and st.session_state["page_control"] == 2):
        last_page()

    else:
        st.session_state["page_control"] = 0
        first_page()


if __name__ == "__main__":
    main()
