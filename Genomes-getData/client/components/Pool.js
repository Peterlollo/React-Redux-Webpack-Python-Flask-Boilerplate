import React, { Component } from 'react';


export default class Pool extends Component {
  constructor(props) {
    super(props);
    console.log('in pool with this this: ', this);
  }
  render() {
    return (
      <h1>Big Face + results { this.props.results }</h1>
    );
  }
}
