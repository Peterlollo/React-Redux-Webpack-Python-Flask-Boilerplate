import * as actionTypes from '../actionTypes/actionTypes.js';
import { combineReducers } from 'redux';

/** REDUCERS ***
Reducers change state based on the execution of an actionCreator. State is described in an object, which changes
based on user interactions. Reducers should not mutate its' arguments or perform API calls (Those are done in actionCreators)
Using Object.assign(), we are able to create a copy of state, and change the previous 'state' to the new 'spread' state (...state)*/

const DEFAULT_STATE = {
  results: [],
};

export const getData = (state = DEFAULT_STATE, action) => {
  switch (action.type) {
  case actionTypes.GET_USER:
    return state;
  case actionTypes.GET_USER_SUCCESS:
    return Object.assign({}, state, {
      ...state,
      results: action.results,
    });
  case actionTypes.GET_USER_FAILURE:
    return Object.assign({}, state, {
      ...state,
      results: action.results,
    });
  default:
    return state;
  }
};

export const currentData = (state = { }, action) => {
    switch (action.type) {
    case actionTypes.GET_USER_FAILURE:
    case actionTypes.GET_USER_SUCCESS:
    case actionTypes.GET_USER:
      return Object.assign({}, state, {
        [action.results]: getData(state[action.results], action)
      })
    default:
      return state
  }
}

const reducers = combineReducers({
  currentData
});

export default reducers;