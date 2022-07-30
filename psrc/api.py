import json

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import bokeh
from bokeh.models import CustomJS
from bokeh.events import DoubleTap
from bokeh.layouts import gridplot
from bokeh.models import Model

from backtesting import Strategy, Backtest
from backtesting.test import GOOG, EURUSD

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        )


class MyStrategy(Strategy):

    def init(self):
        pass

    def next(self):
        pass


def clear_ids(fig):
    for model in fig.select({'type': Model}):
        prev_doc = model.document
        model._document = None
        if prev_doc:
            prev_doc.remove_root(model)


@app.get('/plot')
def get_plot():
    bt1 = Backtest(GOOG.head(1000), MyStrategy)
    bt1.run()
    fig1 = bt1.plot()
    clear_ids(fig1)
    p1 = fig1.children[0].children[0][0]
    p1.js_on_event(DoubleTap, CustomJS(args=dict(p=p1), code='p.reset.emit()'))

    bt2 = Backtest(EURUSD.head(1000), MyStrategy)
    bt2.run()
    fig2 = bt2.plot()
    clear_ids(fig2)
    p2 = fig2.children[0].children[0][0]
    p2.js_on_event(DoubleTap, CustomJS(args=dict(p=p2), code='p.reset.emit()'))

    grid = gridplot([fig1, fig2], ncols=1, sizing_mode='stretch_width')

    return json.dumps(bokeh.embed.json_item(grid))
