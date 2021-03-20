import React from 'react';
import logo from './logo.svg';
import './App.css';

import {NogginsComponent} from './noggins'


function App() {
  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <div>
         <NogginsComponent />  
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          react link
        </a>
      </header>
    </div>
  );
}

export default App;
