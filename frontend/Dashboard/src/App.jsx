import React, { useEffect } from 'react'

function App() {
  useEffect (async () => {
    const res = await axios.get('http://api-data')
    const data = res.data
  })
  return (
    <div className='bg-zinc-800 h-screen w-full'>
      <div className='flex item-center justify-center '>
        <h1 className='text-white font-semibold font-sans mt-5 text-2xl'>Dashboard</h1>
      </div>
      
    </div>
  )
}

export default App
