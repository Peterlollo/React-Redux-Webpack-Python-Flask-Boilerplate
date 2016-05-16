'use strict';
import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import Index from './containers/Index.js';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import reducers from './reducers/index.js';
import thunk from 'redux-thunk';
import createLogger from 'redux-logger';
import promise from 'redux-promise';

/** STORE
Store brings actions, action creators, and reducers all together. They hold the current application state, update
the state with dispatch, and registers listeners.

We use middleware "thunk" so that action creators can return functions, rather than actions.
A "Thunk" basically allows functions to be created that can later be executed.
Essentially, a thunk is a function that returns a function that. This allows for asynchronous functions to be
dispatched as if they were synchronous!

 * @see {@link https://github.com/gaearon/redux-thunk} for further information
**/

const createStoreWithMiddleware = applyMiddleware(
  thunk,
  promise,
  createLogger()
)(createStore);
const store = createStoreWithMiddleware(reducers);

ReactDOM.render(
  <Provider store={store}>
    <Index />
  </Provider>,
  document.getElementById('root')
);
