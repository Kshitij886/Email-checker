import React from "react";
import { useEffect, useState } from "react";
import axios from 'axios'

function App() {
  const [currentDate, setCurrentDate] = useState('');
  const [firewall, setFirewall] = useState(true);
  const [statusF, setStatusF] = useState(false)
  
  const button = async () => {
    setFirewall(!firewall)
    setStatusF(!statusF)
    localStorage.setItem("status", statusF)
    console.log(firewall)
    try {
      const response = await axios.post('http://localhost:5000/api-firewall',{status :firewall});
    } catch (error) {
      console.log('Error: ', error.message)
    }

  }
  useEffect(() => {
    const ButtonStatus = localStorage.getItem('status');
    setStatusF(ButtonStatus)
  },[])

  useEffect(() => {
    const updateDate = () => {
      const now = new Date();
      const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wenesday', 'Thursday', 'Friday', 'Satday'];
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

      const dayOfWeek = weekdays[now.getDay()];
      const dayOfMonth = now.getDate();
      const month = months[now.getMonth()];

      const formattedDate = `${dayOfWeek} ${dayOfMonth} ${month}`;
      setCurrentDate(formattedDate);
    };
    updateDate();
    const now = new Date();
    const midnight = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0);
    const timeUntilMidnight = midnight.getTime() - now.getTime();

    const timeoutId = setTimeout(() => {
      updateDate();
      setInterval(updateDate, 24 * 60 * 60 * 1000);
    }, timeUntilMidnight);

    return () => clearTimeout(timeoutId);
  }, []); 

  return (
    <div className="min-h-screen">
      <header
        className="absolute top-0 left-0 w-full h-27 bg-[#271354] p-4"
        style={{ WebkitAppRegion: "drag" }}
      >
        <div className="inline-block" style={{ WebkitAppRegion: "no-drag" }}>
          <span className="text-lg text-[#7a44e5] leading-none font-sans">
            darkscout
          </span>
        </div>
        <div className="float-right">
          <button
            style={{ WebkitAppRegion: "no-drag" }}
            className="pl-1 mr-2 pr-1 pb-1 text-white text-2xl focus:outline-none"
          >
            –
          </button>
          <button
            style={{ WebkitAppRegion: "no-drag" }}
            className="mr-3 text-white text-2xl focus:outline-none"
          >
            ×
          </button>
        </div>
        <div className="flex item-center justify-center p-4 ">
            <label className="text-white text-center font-sans font-semibold text-3xl ml-10">
              darkscout
            </label>
          </div>
      </header>
      <div className="bg-[#100f18] h-screen mt-20 ">
        <div className="gap-20 flex flex-col items-center justify-between p-4">
      <div className="h-suto w-auto mt-30 bg-[#1a182b] p-2.5 rounded-full">
        <label className="text-gray-400">
          {currentDate}
        </label>
      </div>
      <div className="w-auto h-auto m-0 ">
        <div className="ml-5  bg-[#4a21a2] rounded-full flex items-center justify-center h-12 w-40 p-2">
          <label className="inline-flex items-center cursor-pointer">
            <input type="checkbox" value="" className="sr-only peer" onClick={button} checked = {statusF}/>
            <div className="relative w-14 h-7 bg-[#26175C] rounded-full dark:bg-[#26175C] peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full after:content-[''] after:absolute after:top-0.5 after:start-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
            <span className="ms-3 text-lg font-semibold font-sans text-white">
              Enable
            </span>
          </label>
        </div>

      </div>
        
      </div>

      </div>
     
    </div>
  );
}

export default App;
