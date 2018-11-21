import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

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
    var server_settings = {
      url: 'http://127.0.0.1:5000/',
      process: './process'
    };

    var onprocessfile = (error, res) => {
      let res_json = JSON.parse(res['serverId']);
      if(res_json['status'] == 1) {
        let result = res_json['result']
        this.setState({results: result});
        this.setState({processed: true});
      }
    }

    return (
      <div className="main-container">
       <header>
         <h1>Caribbean Classifier 🎵🎶🤔</h1>
        </header>
        <p>
          Upload your caribbean music to instantly identify the
            <a className="intro-bold-link red"><span> genre</span></a>,
            <a className="intro-bold-link green"><span> instruments</span></a>, and
            <a className="intro-bold-link blue"><span> beat structure</span></a>.<br/>
          Our <i>recurrent neural net</i> models are trained from thousands of Caribbean songs.
        </p>
        <hr />
        <h3>1. Upload audio</h3>
        <div className="upload-container">
          <div className="upload"><FilePond onprocessfile={onprocessfile} server={server_settings}/></div>
        </div>
        <hr />
        <h3>2. Review results</h3>
        <div className="results-container">
          <ClassificationResults processed={this.state.processed} results={this.state.results}/>
        </div>
      </div>
    );
  }
}

class ClassificationResults extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    if (this.props.processed) {
      var results = this.props.results
      var predictedclass = results['predicted_class']
      var probability = results['probability']
      var description = results['description']
      return (
        <div className="classification-results">
          <div className="result-title"><strong>{predictedclass}</strong> - Confidence: {probability}%</div>
          <p>{description}</p>
        </div>
      );
    } else {
      return (<div><i>Upload files to begin - Classification results will show up here</i></div>);
    }
  };
}

export default App;
