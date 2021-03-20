import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {ProfileBadgeComponent} from './profiles'
import {FeedComponent, NogginsComponent, NogginDetailComponent} from './noggins'
import * as serviceWorker from './serviceWorker';

const appEl = document.getElementById('root')
if (appEl) {
  ReactDOM.render(<App />, appEl);
}

const e = React.createElement
const nogginsEl = document.getElementById('tossiteh') 
if (nogginsEl) {
  ReactDOM.render(
    e(NogginsComponent, nogginsEl.dataset), nogginsEl);
}

const nogginsFeedEl = document.getElementById('tossiteh-feed') 
if (nogginsFeedEl) {
  ReactDOM.render(
    e(FeedComponent, nogginsFeedEl.dataset), nogginsFeedEl);
}

const nogginDetailElements = document.querySelectorAll(".tossiteh-detail")

nogginDetailElements.forEach(container=> {
  ReactDOM.render(
    e(NogginDetailComponent, container.dataset),
    container);
})

const userProfileBadgeElements = document.querySelectorAll(".tossiteh-profile-badge")

userProfileBadgeElements.forEach(container=> {
  ReactDOM.render(
    e(ProfileBadgeComponent, container.dataset),
    container);
})



// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
