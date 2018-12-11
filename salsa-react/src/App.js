import React, { Component } from 'react';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';
import PieChart from 'react-minimal-pie-chart';

class App extends Component {
  constructor() {
    super()
    this.state = {
      processed: false,
      results: null
    }
  }

  render() {
    const server_settings = {
      url: 'http://104.248.235.168/api',
      process: '/process'
    };

    const onprocessfile = (error, res) => {
      const res_json = JSON.parse(res['serverId']);
      try {
        if(res_json['status'] === 1) {
          const result = res_json['result']
          this.setState({results: result});
          this.setState({processed: true});
        }
      } catch(e) {}
    }

    return (
      <div className="main-container">
        <header>
          <h1>A Caribbean Music Classifier <span role="img" aria-label='emojis'>🌴💃🎵🎶🤔</span></h1>
        </header>
        <p className="intro">
          Upload your Caribbean music to instantly identify the genre: <a href="/#" className="intro-bold-link">salsa</a>, <a href="/#" className="intro-bold-link">soca</a>, and <a href="/#" className="intro-bold-link">reggae</a>.
          Our <i>recurrent neural net</i> models are trained with hundreds of Caribbean songs.
        </p>
        <hr />
        <h3>1. Upload audio</h3>
        <div className="upload-container">
          <div className="upload"><FilePond onprocessfile={onprocessfile} server={server_settings}/></div>
        </div>
        <hr />
        <h3>2. Review results</h3>
        <div className="results-container">
          <Results processed={this.state.processed} results={this.state.results}/>
        </div>
      </div>
    );
  }
} // App

const Results = ({processed, results}) => {
  if (processed) {
/*    const probstr = results.allprobs.substring(1, results.allprobs.length - 1);
    const reggae_prob = parseFloat(probstr.split(', ')[0]);
    const soca_prob = parseFloat(probstr.split(', ')[1]);
    const salsa_prob = parseFloat(probstr.split(', ')[2]);*/
    const probs = results.allprobs;
    const reggae_prob = parseFloat(probs[0]);
    const salsa_prob = parseFloat(probs[1]);
    const soca_prob = parseFloat(probs[2]);
    return (
      <div className="classification-results">
        <div className="result-title">
          <b>{results.predicted_class}</b> - Confidence: {results.probability}%
        </div>
        <p>{results.description}</p>
	<div className="pie-container">
	<div className="pie-left">	
	  <p> <strong>Reggae<span style={{color:"#ccff90"}}>◼</span>: </strong>{reggae_prob}%<br /> <strong>Soca<span style={{color:"#a7ffeb"}}>◼</span>: </strong>{soca_prob}%<br /> <strong>Salsa<span style={{color:"#80d8ff"}}>◼</span>: </strong>{salsa_prob}% </p>
	</div>
	<div className="pie-right">
	<div class="pie-chart" animate={true} animationDuratoin={500}><PieChart
	  data={[
	    { title: 'Reggae', value: Math.round(reggae_prob), color: '#ccff90' },
	    { title: 'Soca', value: Math.round(soca_prob), color: '#a7ffeb' },
	    { title: 'Salsa', value: Math.round(salsa_prob), color: '#80d8ff' },
	  ]}
	/></div>
	</div>
	</div>
      </div>

    );
  } else {
    return (
      <div><i>Upload files to begin - Classification results will show up here</i></div>
    );
  }
};

export default App;
