import numpy as np
from ipycanvas import Canvas
from ipywidgets import Dropdown, IntSlider, FloatSlider, Button, HBox, VBox, Output, Layout
from pynq import allocate



def create_trochoid_ui(dma, canvas_width=800, canvas_height=600):
    # Canvas and state
    canvas = Canvas(width=canvas_width, height=canvas_height)
    offset_x = 0.0
    offset_y = 0.0
    scale = 1.0
    output = Output()

    # Controls
    type_dropdown = Dropdown(options=['Hypotrochoid', 'Epitrochoid'], value='Hypotrochoid', description='Type:')
    R_slider = IntSlider(value=5, min=-31, max=31, step=1, description='R:')
    r_slider = IntSlider(value=3, min=-31, max=31, step=1, description='r:')
    d_slider = IntSlider(value=5, min=-31, max=31, step=1, description='d:')
    points_slider = IntSlider(value=500, min=1, max=1023, step=1, description='Points:')
    pan_interval_slider = FloatSlider(value=1.0, min=0.01, max=100.0, step=0.01, description='Pan interval:')
    zoom_slider = FloatSlider(value=1.2, min=1.01, max=10.0, step=0.01, description='Zoom factor:')

    btn_pan_left = Button(description='Pan Left')
    btn_pan_right = Button(description='Pan Right')
    btn_pan_up = Button(description='Pan Up')
    btn_pan_down = Button(description='Pan Down')
    btn_zoom_in = Button(description='Zoom In')
    btn_zoom_out = Button(description='Zoom Out')

    def fetch_trochoid(R, r, d, num_points, trochoid_type):
        word = 0 if trochoid_type == 'Epitrochoid' else 1
        word = (word << 7) | (R & 0x7F)
        word = (word << 7) | (r & 0x7F)
        word = (word << 7) | (d & 0x7F)
        word = (word << 10) | num_points
        in_buffer = allocate(shape=(256,), dtype=np.uint32)
        out_buffer = allocate(shape=(256,), dtype=np.uint32)
        in_buffer[:] = word
        dma.sendchannel.transfer(in_buffer)
        dma.recvchannel.transfer(out_buffer)
        dma.sendchannel.wait()
        dma.recvchannel.wait()
        x = ((out_buffer >> 16) & 0xFFFF).astype(np.int32)
        y = (out_buffer & 0xFFFF).astype(np.int32)
        return x, y

    def redraw(change=None):
        nonlocal offset_x, offset_y, scale
        canvas.clear()
        R = R_slider.value
        r = r_slider.value
        d = d_slider.value
        pts = points_slider.value
        tp = type_dropdown.value
        x, y = fetch_trochoid(R, r, d, pts, tp)
        cx, cy = canvas_width / 2, canvas_height / 2
        xs = (x * scale) + cx + offset_x
        ys = (y * scale) + cy + offset_y
        canvas.stroke_style = 'black'
        canvas.begin_path()
        canvas.move_to(xs[0], ys[0])
        for xi, yi in zip(xs[1:], ys[1:]):
            canvas.line_to(xi, yi)
        canvas.stroke()

        with output:
            output.clear_output()
            print(f"{tp} (R={R}, r={r}, d={d}, pts={pts})")

    # Pan/zoom
    def pan_left(b):
        nonlocal offset_x
        offset_x -= pan_interval_slider.value
        redraw()
    def pan_right(b):
        nonlocal offset_x
        offset_x += pan_interval_slider.value
        redraw()
    def pan_up(b):
        nonlocal offset_y
        offset_y -= pan_interval_slider.value
        redraw()
    def pan_down(b):
        nonlocal offset_y
        offset_y += pan_interval_slider.value
        redraw()
    def zoom_in(b):
        nonlocal scale
        scale *= zoom_slider.value
        redraw()
    def zoom_out(b):
        nonlocal scale
        scale /= zoom_slider.value
        redraw()

    for w in [type_dropdown, R_slider, r_slider, d_slider, points_slider]:
        w.observe(redraw, names='value')
    btn_pan_left.on_click(pan_left)
    btn_pan_right.on_click(pan_right)
    btn_pan_up.on_click(pan_up)
    btn_pan_down.on_click(pan_down)
    btn_zoom_in.on_click(zoom_in)
    btn_zoom_out.on_click(zoom_out)
    top_controls = HBox([type_dropdown, R_slider, r_slider, d_slider, points_slider])
    pan_controls = HBox([btn_pan_left, btn_pan_right, btn_pan_up, btn_pan_down, pan_interval_slider])
    zoom_controls = HBox([btn_zoom_in, btn_zoom_out, zoom_slider])

    row_layout = Layout(display='flex', flex_flow='row wrap', align_items='center', overflow='auto', width='100%')
    top_controls = HBox([type_dropdown, R_slider, r_slider, d_slider, points_slider], layout=row_layout)
    pan_controls = HBox([btn_pan_left, btn_pan_right, btn_pan_up, btn_pan_down, pan_interval_slider], layout=row_layout)
    zoom_controls = HBox([btn_zoom_in, btn_zoom_out, zoom_slider], layout=row_layout)

    ui = VBox([top_controls, pan_controls, zoom_controls, canvas, output])
    redraw()
    return ui