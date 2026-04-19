loginWidget_style = """
QPushButton { font-size: 12px; 
            padding : 2px;
            padding-left : 4px;  /* 左边距 */
            padding-right : 4px;  /* 左边距 */
            height : 18px;}
QPushButton:checked {

    border: 2px solid green; /* 当按钮被选中时，边框颜色改为绿色 */
    color: black; /* 文本颜色设置为黑色 */
    background-color: #a8d7b6; /* 被选中的按钮背景色为浅绿色 */
}
QPushButton:!checked {
    border: 2px solid #5c5c5c; /* 设置边框为2像素宽，实线，并使用灰色 */
    color: black; /* 文本颜色设置为黑色 */
    background-color: lightgray; /* 背景色设置为浅灰色 */
}
"""