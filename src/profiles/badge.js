import React, { useEffect, useState} from 'react'

import {UserDisplay, BiggerPicture, FlwLink, FlwrLink} from './components'
import {apiProfileDetail, apiProfileFollowToggle} from './lookup'
import {DisplayCount} from './utils'


function ProfileBadge(props) {
  const {user, didFollowToggle, profileLoading} = props
  let currentVerb = (user && user.is_following) ? "unfollow" : "follow"
  currentVerb = profileLoading ? "one moment ... " : currentVerb
  // const followingCount = user.following_count
  // const followerCount = user.follower_count
  // const requestUser = user.username
  // console.log(requestUser)
 
  const handleFollowToggle = (event) => {
    event.preventDefault()
    console.log("CURRENT USERS ID: "+ user.followers)
    if (didFollowToggle && !profileLoading) {
      didFollowToggle(currentVerb)
    }
  }
  return user ? <center>
    <div className='container'>
      <span style={{"display":"block"}}><BiggerPicture user={user}/><UserDisplay user={user} includeFullName /></span>
        <center className="container">
          <div style={{"display":"inline-block"}}>
            <img style={{"opacity":"0.7","width":"30px","height":"30px","float":"left","transform":"rotate(20deg)"}} src='https://noggintoss.com/media/react/look.png' alt='locationmark' />
        <p style={{"float":"right"}} className='small text-muted mt-3'>{user.location}</p></div>
      </center>
      <span style={{"display":"block"}}>
        <FlwrLink user={user}><h4><DisplayCount>{user.follower_count}</DisplayCount> {user.follower_count === 1 ? "🇫🇴🇱🇱🇴🇼🇪🇷" : "🇫🇴🇱🇱🇴🇼🇪🇷🇸"} </h4></FlwrLink>
        <FlwLink user={user}><h4> {"🇫🇴🇱🇱🇴🇼🇮🇳🇬"} <DisplayCount>{user.following_count}</DisplayCount> </h4></FlwLink></span>
      <div className='container' style={{"width":"600px"}}>
        <hr style={{"width":"250px"}}></hr>
        <div style={{"width":"500px"}}><h6 className='container'>{user.bio}</h6></div>
        </div>
        <hr style={{"width":"250px"}}></hr>
      <button style={{"borderRadius":"7%","border":"none"}}
      className='btn btn-outline-info btn-lg' onClick={handleFollowToggle}>
        <h5>{currentVerb}</h5></button> 
    </div>

    </center> : null
}


export function ProfileBadgeComponent (props) {
  const {username} = props
  // spaceR
  const [didLookup, setDidLookup] = useState(false)
  const [profile, setProfile] = useState(null)
  const [profileLoading, setProfileLoading] = useState(false)
  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setProfile(response)
    } else {
      console.log(response.error)
    }
  }
  useEffect(() =>{
    if (didLookup === false) {
      apiProfileDetail(username, handleBackendLookup)
      setDidLookup(true)
    }
  },[username, didLookup, setDidLookup])
  
  const handleNewFollow = (actionVerb) => {
    apiProfileFollowToggle(username, actionVerb, (response, status) => {
      console.log("BADGE CHECK",response, status)
      if (status === 200) {
        setProfile(response)
      } else if (status === 500) {
        window.location.replace("/login"); 
      }
      setProfileLoading(false)
      
    }) 
    setProfileLoading(true)
    
  }  
  return didLookup === false ? <strong>VALIDATING...</strong> : profile ? <ProfileBadge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}/> : null

}
