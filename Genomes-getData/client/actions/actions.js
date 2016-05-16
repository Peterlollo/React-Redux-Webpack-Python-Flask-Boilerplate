import * as actionTypes from '../actionTypes/actionTypes';
import 'whatwg-fetch';

/** ACTIONS ***
Actions define the action type, and do something based on the value of 'type' (i.e. receiveUserData)
Action creators will send information to the 'store', by going through reducers, which will change
 state based on the action type. Action creators (i.e. getUserData) are executable in containers
that use Redux's 'connect' helper. 'bindActionCreators()' binds action creators to dispatch */

/**
  *Default request handler
**/
export const requestUserData = (data) => {
  return {
    type: actionTypes.GET_USER,
    data,
  }
}

/**
  * Receive data from fetch
**/
export const receiveUserData = (data) => {
  return {
    type: actionTypes.GET_USER_SUCCESS,
    results: data,
  }
}

/**
  *Error handling for failed fetch
**/
export const failedFetch = (err) => {
  console.error('in failed fetch with this err: ', err);
  console.dir(err);
  return {
    type: actionTypes.GET_USER_FAILURE,
    err
  }
}

/**
  * Fetch current user's information
**/
export const getUserData = () => {
  console.log('INSIDE GET USER DATA FUNCTION');
  return (dispatch) => {
    dispatch(requestUserData)

    return fetch('/get_info/', {
      method: 'GET',
    }).then(res => res.json())
    .then(json => dispatch(receiveUserData(json)))
    .catch(err => dispatch(failedFetch(err)))
  }
}
