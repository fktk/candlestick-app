import * as Bokeh from '@bokeh/bokehjs'

function App() {
  const handleClick = () => {
    fetch('http://192.168.1.101:8000/plot').then(res => res.json())
      .then(data => {
        Bokeh.embed.embed_item(JSON.parse(data), 'testPlot')

      })
  }

  return (
    <div>
      <button onClick={handleClick} style={{width: '600px'}}>send</button>
      <div id='testPlot' style={{width: '600px'}} className='bk-root'></div>
    </div>
  )
}

export default App
