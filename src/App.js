//import logo from './logo.svg';
import { unstable_renderSubtreeIntoContainer } from 'react-dom';
import './App.css';
import { useEffect, useState } from 'react';
import axios from "axios"

function App() {
  const [data, setData] = useState([{}]);

  // const [file, setFile] = useState(null);
  // const [progress, setProgress] = useState({started: false, pc: 0})
  // const [msg, setMsg] = useState(null)

  // function handleUpload(){
  //   if(!file){
  //     console.log("No file selected")
  //   }

  //   const fd = new FormData()
  //   fd.append('file', file)
  //   console.log("JJOJO" +fd)

  //   axios.post('http://httpbin.org/post', fd, {
  //     onUploadProgress: (progressEvent) => {console.log(progressEvent.progress *100)},
  //     headers: {
  //       "Custom-Header": "value",
  //     }
  //   }).then(res => {
  //     setMsg("Upload successful")
  //     console.log(res.data)
  //   })
  //   .catch(err => console.log(err));
  // }

  // return (
  //   <div className="App">
  //     {/* <header className="App-header">
  //       <img src={logo} className="App-logo" alt="logo" />
  //       <p>
  //         Edit <code>src/App.js</code> and save to reload.
  //       </p>
  //       <a
  //         className="App-link"
  //         href="https://reactjs.org"
  //         target="_blank"
  //         rel="noopener noreferrer"
  //       >
  //         Learn React
  //       </a>
  //     </header> */}
  //     <h1>
  //       Uploading Files in React
  //     </h1>

  //     <input onChange={
  //        (e) => {
  //         setFile(e.target.files[0]);
  //        }
  //     } type='file'/> 

  //     <button onClick={handleUpload}>
  //       Upload
  //     </button>

  //   </div>
  // );

  
  useEffect(() => {
    // Fetch data from the backend
    fetch('http://127.0.0.1:5000/members')
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

  return (
    <div>
      <h1>Data from the Backend:</h1>

      {(typeof data.members === 'undefined') ? (
        <p>Loading...</p>
      ) : 
      <ul>
        {data.members.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
      } 
    </div>
  );
}

export default App;
