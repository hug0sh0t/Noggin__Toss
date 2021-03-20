import React from 'react'

export function UserLink (props) {
  const {username} = props
  const handleUserLink = (event) => {
    window.location.href = `/profiles/${username}`
  }

  return <span className='pointer' onClick={handleUserLink}>
    {props.children}
  </span>
}

export function FlwLink (props) {
  const {user} = props
  const handleUserLink = (event) => {
    window.location.href = `/following/?followers=${user.followers}`
  }

  return <span className='pointer' onClick={handleUserLink}>
    {props.children}
  </span>
}


export function FlwrLink (props) {
  const {user} = props
  const handleUserLink = (event) => {
    window.location.href = `/profiles/${user.username}/followers`
  }

  return <span className='pointer' onClick={handleUserLink}>
    {props.children}
  </span>
}



export function UserDisplay(props) {
  const {user, includeFullName, hideLink} = props
  const nameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name} ` : null

  return <React.Fragment>
    <div className="container" style={{"color":"#ff9999"}}><h6>{nameDisplay}
      <img style={{"width":"30px","height":"30px;float:left"}} src='https://noggintoss.com/media/react/bottt.png' alt='cloud'/>
       @{user.username}
    </h6></div>
    {hideLink === true ? <h6>react>> {user.username} </h6> :<UserLink username={user.username}></UserLink>}
  </React.Fragment>
}

//<span className='mx-1 px-3 py-2 small rounded-circle bg-light text-dark'>{"🗲 "+user.username[0]}</span>

// feed avatar size
export function UserPicture (props) {
  const {user, hideLink} = props
  const userIdSpan = <img className="shadow-lg zoom" 
    style={{"borderRadius":"50%", "width":"90px","height":"90px","background":"none","padding":"0"}} src={user.avatar} alt='NOGGINAVATAR'/>
    return hideLink === true ? userIdSpan : <div><UserLink username={user.username}>{userIdSpan}</UserLink></div>
}



//profile avatar size
export function BiggerPicture (props) {
  const {user, hideLink} = props
  const userIdSpan = <img className="" style={{"borderRadius":"50%", "width":"250px","height":"250px","border":"4px solid #c8c8c8c8"}} src={user.avatar} alt='NOGGINAVATAR'/>
    return hideLink === true ? userIdSpan : <div><UserLink username={user.username}>{userIdSpan}</UserLink></div>
}
