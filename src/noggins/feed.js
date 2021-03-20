import React, {useEffect, useState} from 'react'

import {apiNogginFeed} from './lookup'

import {Noggin} from './detail'


export function FeedList(props) {
  const [nogginsInit, setNogginsInit] = useState([])
  const [noggins, setNoggins] = useState([])
  const [nextUrl, setNextUrl] = useState(null)
  const [nogginsDidSet, setNogginsDidSet] = useState(false)
  useEffect(()=>{
    const final = [...props.newNoggins].concat(nogginsInit)
    if (final.length !== noggins.length) {
      setNoggins(final)
    }
  }, [props.newNoggins, noggins, nogginsInit])

  useEffect(() => {
    if (nogginsDidSet === false) {
      const handleNogginListLookup = (response, status) => {
        if (status === 200) {
          setNextUrl(response.next)
          setNogginsInit(response.results)
          setNogginsDidSet(true)
        } // old alert else error
      }
      apiNogginFeed(handleNogginListLookup)
    }
  }, [nogginsInit, nogginsDidSet, setNogginsDidSet, props.username])

  const handleDidRelay = (newNoggin) => {
    const updateNogginsInit = [...nogginsInit]
    updateNogginsInit.unshift(newNoggin)
    setNogginsInit(updateNogginsInit)
    const updateFinalNoggins = [...noggins]
    updateFinalNoggins.unshift(noggins)
    setNoggins(updateFinalNoggins)
  }
  const handleLoadNext = (event) => {
    event.preventDefault()
    if (nextUrl !== null) {
      const handleLoadNextResponse = (response, status) =>{
        if (status === 200) {
          setNextUrl(response.next)
          const newNoggins = [...noggins].concat(response.results)
          setNogginsInit(newNoggins)
          setNoggins(newNoggins)
        } // old alert else error
      }
      apiNogginFeed(handleLoadNextResponse, nextUrl)
    }
  }



  return <React.Fragment>{noggins.map((item, index)=>{
    return <Noggin
    noggin={item}
    didRelay={handleDidRelay}
    className='my-5 py-5 bg-white text-dark'
    key={`${index}-{item.id}`}  />
  })}
    {nextUrl !== null && <center><button onClick={handleLoadNext}
      style={{"boxShadow":"none","border":"none","padding":"0","background":"none"}} className='zoom btn btn-outline-light mb-3'>
      <img src="https://noggintoss.com/media/react/more.png" style={{"width":"50px","height":"50px",}} alt='more'/></button></center> }
  </React.Fragment>
}


