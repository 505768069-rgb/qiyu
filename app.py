# -*- coding: utf-8 -*-
"""
奇遇 - 让命运来决定
"""

from nicegui import ui
import random

DEFAULT_DATA = {
    "吃什么": ["火锅", "烧烤", "麻辣烫", "炸鸡", "披萨", "寿司", "拉面", "汉堡", "饺子", "米线",
              "螺蛳粉", "黄焖鸡", "麻辣香锅", "串串", "烤鱼", "牛排", "日料", "韩餐", "泰餐", "西餐"],
    "去哪玩": ["看电影", "逛街", "公园散步", "唱K", "密室逃脱", "剧本杀", "桌游", "网吧", "咖啡厅", "图书馆",
              "健身房", "游泳", "爬山", "骑行", "钓鱼", "野餐", "博物馆", "游乐园", "动物园", "宅家"],
    "自定义": []
}

@ui.page('/')
def main_page():
    ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="奇遇">
    <meta name="theme-color" content="#667eea">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        * { font-family: 'Noto Sans SC', sans-serif; -webkit-tap-highlight-color: transparent; }
        body { overscroll-behavior: none; }
        .bg-main {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 50%, #fcd34d 100%);
            min-height: 100vh;
        }
        .premium-card {
            background: rgba(255,255,255,0.35) !important;
            backdrop-filter: blur(12px);
            border-radius: 24px !important;
            border: 1px solid rgba(255,255,255,0.4) !important;
        }
        .tag-btn {
            background: linear-gradient(135deg, rgba(102,126,234,0.8) 0%, rgba(118,75,162,0.8) 100%);
            border: none !important;
            border-radius: 50px !important;
            padding: 10px 24px !important;
            color: white !important;
            font-weight: 500 !important;
        }
        .tag-btn:active { transform: scale(0.95); }
        .tag-btn-inactive {
            background: rgba(255,255,255,0.35) !important;
            color: #5a4a78 !important;
        }
        .draw-btn {
            background: linear-gradient(-45deg, rgba(238,119,82,0.85), rgba(231,60,126,0.85), rgba(35,166,213,0.85), rgba(35,213,171,0.85));
            background-size: 400% 400%;
            animation: gradient 3s ease infinite;
            border: none !important;
            border-radius: 60px !important;
            padding: 20px 48px !important;
            color: white !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }
        .draw-btn:active { transform: scale(0.95); }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .retry-btn {
            background: rgba(255,255,255,0.35) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 50px !important;
            color: #5a4a78 !important;
        }
        .result-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .app-title {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 2rem;
        }
    </style>
    ''')
    
    app_data = DEFAULT_DATA.copy()
    current_category = {'value': list(app_data.keys())[0]}
    result_label = None
    
    with ui.column().classes('w-full min-h-screen items-center p-4 bg-main'):
        
        ui.html('<div class="app-title">奇遇</div>', sanitize=False)
        ui.label('让命运来决定').classes('text-lg text-purple-600/80 mb-8 font-medium')
        
        with ui.row().classes('gap-3 mb-6 flex-wrap justify-center'):
            def select_category(cat):
                current_category['value'] = cat
                for btn, c in zip(category_buttons, app_data.keys()):
                    if c == cat:
                        btn._classes = [x for x in btn._classes if 'tag-btn-inactive' not in x]
                        btn.classes(add='tag-btn')
                    else:
                        btn._classes = [x for x in btn._classes if x != 'tag-btn']
                        btn.classes(add='tag-btn tag-btn-inactive')
                    btn.update()
            
            category_buttons = []
            first_cat = list(app_data.keys())[0]
            for cat in app_data.keys():
                btn = ui.button(cat, on_click=lambda c=cat: select_category(c)).classes(
                    'tag-btn' if cat == first_cat else 'tag-btn tag-btn-inactive'
                ).props('flat')
                category_buttons.append(btn)
        
        with ui.card().classes('w-full max-w-sm premium-card p-8 text-center'):
            result_label = ui.label('点击下方按钮抽签').classes('text-2xl font-bold min-h-[80px] flex items-center justify-center result-text')
        
        def do_draw():
            category = current_category['value']
            options = app_data.get(category, [])
            if not options:
                result_label.set_text('该分类没有选项')
                return
            
            async def animate():
                for i in range(15):
                    result_label.set_text(random.choice(options))
                    await ui.run_javascript('void(0)', timeout=0.05)
                final = random.choice(options)
                result_label.set_text(final)
                ui.notify(f'就决定是 {final} 了！', type='positive', position='top')
            
            ui.timer(0, animate, once=True)
        
        ui.button('开始抽签', on_click=do_draw).classes('draw-btn mt-6').props('flat')
        ui.button('再来一次', on_click=do_draw).classes('retry-btn mt-3 px-6 py-2').props('flat')

ui.run(title='奇遇', port=7860, host='0.0.0.0')
