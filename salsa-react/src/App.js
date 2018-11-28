import React, { Component } from 'react';
import { FilePond } from 'react-filepond';
import 'filepond/dist/filepond.min.css';

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
      url: 'http://127.0.0.1:5000/',
      process: './process'
    };

    const onprocessfile = (error, res) => {
      const res_json = JSON.parse(res['serverId']);
      if(res_json['status'] === 1) {
        const result = res_json['result']
        this.setState({results: result});
        this.setState({processed: true});
      }
    }

    return (
      <div className="main-container">
        <header>
          <h1>A Caribbean Music Classifier <span role="img" aria-label='emojis'>🌴💃🎵🎶🤔</span></h1>
        </header>
        <p className="intro">
          Upload your caribbean music to instantly identify the <a href="/#" className="intro-bold-link">genre</a>, <a href="/#" className="intro-bold-link">instruments</a>, and <a href="/#" className="intro-bold-link">rhythm</a>.
          Our <i>recurrent neural net</i> models are trained with thousands of Caribbean songs.
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
    return (
      <div className="classification-results">
        <div className="result-title">
          <b>{results.predicted_class}</b> - Confidence: {results.probability}%
        </div>
        <p>{results.description}</p>
      </div>
    );
  } else {
    return (
      <div><i>Upload files to begin - Classification results will show up here</i></div>
    );
  }
};

export default App;
