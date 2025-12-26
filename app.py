# -*- coding: utf-8 -*-
"""
奇遇 - 让命运来决定
"""

from nicegui import ui, app
import random
import json
import os

# 数据存储（部署环境用内存存储）
DEFAULT_DATA = {
    "吃什么": ["火锅", "烧烤", "麻辣烫", "炸鸡", "披萨", "寿司", "拉面", "汉堡", "饺子", "米线",
              "螺蛳粉", "黄焖鸡", "麻辣香锅", "串串", "烤鱼", "牛排", "日料", "韩餐", "泰餐", "西餐"],
    "去哪玩": ["看电影", "逛街", "公园散步", "唱K", "密室逃脱", "剧本杀", "桌游", "网吧", "咖啡厅", "图书馆",
              "健身房", "游泳", "爬山", "骑行", "钓鱼", "野餐", "博物馆", "游乐园", "动物园", "宅家"],
    "自定义": []
}

@ui.page('/')
def main_page():
    # 每个用户独立的数据（存在浏览器localStorage）
    ui.add_head_html('''
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="奇遇">
    <meta name="theme-color" content="#667eea">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    ''')
    
    ui.add_head_html('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        * { font-family: 'Noto Sans SC', sans-serif; -webkit-tap-highlight-color: transparent; }
        body { overscroll-behavior: none; }
        .bg-main {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 50%, #fcd34d 100%);
            min-height: 100vh;
            padding-bottom: env(safe-area-inset-bottom);
        }
        .premium-card {
            background: rgba(255,255,255,0.35) !important;
            backdrop-filter: blur(12px) saturate(120%);
            -webkit-backdrop-filter: blur(12px) saturate(120%);
            border-radius: 24px !important;
            border: 1px solid rgba(255,255,255,0.4) !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
        }
        .tag-btn {
            background: linear-gradient(135deg, rgba(102,126,234,0.8) 0%, rgba(118,75,162,0.8) 100%);
            border: none !important;
            border-radius: 50px !important;
            padding: 10px 24px !important;
            color: white !important;
            font-weight: 500 !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
            transition: all 0.3s ease !important;
        }
        .tag-btn:active { transform: scale(0.95); }
        .tag-btn-inactive {
            background: rgba(255,255,255,0.35) !important;
            backdrop-filter: blur(8px);
            color: #5a4a78 !important;
            box-shadow: none;
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
            box-shadow: 0 6px 25px rgba(231, 60, 126, 0.3);
            transition: all 0.2s ease !important;
        }
        .draw-btn:active { transform: scale(0.95); }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .retry-btn {
            background: rgba(255,255,255,0.35) !important;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 50px !important;
            color: #5a4a78 !important;
            font-weight: 500 !important;
        }
        .result-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .premium-input .q-field__control {
            background: rgba(255,255,255,0.35) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
        }
        .premium-select .q-field__control {
            background: rgba(255,255,255,0.35) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
        }
        .premium-select .q-icon { font-family: 'Material Icons' !important; }
        .add-btn {
            background: linear-gradient(135deg, rgba(102,126,234,0.75) 0%, rgba(118,75,162,0.75) 100%) !important;
            border: none !important;
            border-radius: 16px !important;
            color: white !important;
            font-weight: 500 !important;
        }
        .option-item {
            background: rgba(255,255,255,0.3) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .del-btn { color: #e73c7e !important; opacity: 0.6; }
        .premium-expansion {
            background: rgba(255,255,255,0.3) !important;
            backdrop-filter: blur(12px);
            border-radius: 20px !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
        }
        .premium-expansion .q-expansion-item__container,
        .premium-expansion .q-item { background: transparent !important; border-radius: 20px !important; }
        .fancy-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
            border: none !important;
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
    
    # 使用storage来保存用户数据
    app_data = ui.storage.user.get('qiyu_data', DEFAULT_DATA.copy())
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
                result_label.set_text('该分类没有选项，请先添加！')
                return
            
            async def animate():
                for i in range(15):
                    result_label.set_text(random.choice(options))
                    await ui.run_javascript('void(0)', timeout=0.05)
                final = random.choice(options)
                result_label.set_text(final)
                ui.notify(f'就决定是 {final} 了！', type='positive', position='top', timeout=3000)
            
            ui.timer(0, animate, once=True)
        
        ui.button('开始抽签', on_click=do_draw).classes('draw-btn mt-6').props('flat')
        ui.button('再来一次', on_click=do_draw).classes('retry-btn mt-3 px-6 py-2').props('flat')
        
        ui.html('<div class="fancy-divider w-full max-w-sm my-8"></div>', sanitize=False)
        
        with ui.expansion('管理选项').classes('w-full max-w-sm premium-expansion'):
            
            edit_category = ui.select(
                label='选择分类',
                options=list(app_data.keys()),
                value=list(app_data.keys())[0]
            ).classes('w-full premium-select')
            
            options_container = ui.column().classes('w-full mt-4 gap-2')
            
            def refresh_options():
                options_container.clear()
                with options_container:
                    cat = edit_category.value
                    options = app_data.get(cat, [])
                    
                    if not options:
                        ui.label('暂无选项').classes('text-gray-400 italic text-center py-4')
                    else:
                        for opt in options:
                            with ui.row().classes('w-full items-center justify-between option-item px-4 py-3'):
                                ui.label(opt).classes('text-gray-700 font-medium')
                                
                                def delete_opt(o=opt):
                                    app_data[edit_category.value].remove(o)
                                    ui.storage.user['qiyu_data'] = app_data
                                    refresh_options()
                                    ui.notify(f'已删除: {o}', type='info')
                                
                                ui.button(icon='close', on_click=delete_opt).props('flat round dense').classes('del-btn')
            
            edit_category.on('update:model-value', lambda: refresh_options())
            refresh_options()
            
            ui.html('<div class="fancy-divider w-full my-4"></div>', sanitize=False)
            new_option = ui.input(label='添加新选项', placeholder='输入新选项...').classes('w-full premium-input')
            
            def add_option():
                opt = new_option.value.strip()
                if not opt:
                    ui.notify('请输入选项内容', type='warning')
                    return
                cat = edit_category.value
                if opt in app_data[cat]:
                    ui.notify('该选项已存在', type='warning')
                    return
                app_data[cat].append(opt)
                ui.storage.user['qiyu_data'] = app_data
                new_option.value = ''
                refresh_options()
                ui.notify(f'已添加: {opt}', type='positive')
            
            ui.button('添加选项', on_click=add_option).classes('w-full mt-3 add-btn').props('flat unelevated')
            
            ui.html('<div class="fancy-divider w-full my-4"></div>', sanitize=False)
            new_category = ui.input(label='添加新分类', placeholder='如：周末干嘛').classes('w-full premium-input')
            
            def add_category():
                cat = new_category.value.strip()
                if not cat:
                    ui.notify('请输入分类名称', type='warning')
                    return
                if cat in app_data:
                    ui.notify('该分类已存在', type='warning')
                    return
                app_data[cat] = []
                ui.storage.user['qiyu_data'] = app_data
                new_category.value = ''
                edit_category.options = list(app_data.keys())
                ui.notify(f'已添加分类: {cat}', type='positive')
                ui.navigate.reload()
            
            ui.button('添加分类', on_click=add_category).classes('w-full mt-3 add-btn').props('flat unelevated')
        
        ui.label('可以添加自己常去的餐厅和地点').classes('text-purple-600/70 text-sm mt-8 text-center font-medium')

ui.run(title='奇遇', port=7860, storage_secret='qiyu_secret_key_2024')
