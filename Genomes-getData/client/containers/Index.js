import React, { Component } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import * as Actions from '../actions/actions.js';
import Header from '../components/Header.js';
import Footer from '../components/Footer.js';
import Pool from '../components/Pool.js';

// import component for viewing

export default class Index extends Component {
  constructor(props) {
    super(props)
  }
  componentDidMount() {
    // execute a function from this.props here ex. this.props.requestLogIn
    // this.props.requestLogIn will be imported from actions

    // immediately render getUserData from actions
      // do something with his data
      console.log('THIS IS THIS INSIDE THE INDEX CONTAINER: ', this);
      this.props.actions.getUserData()
  }

  // fancy d3 functions here

  render() {
    const { results } = this.props;
    return (
      <div className='InitialLoad'>
      <Header />
      <h1> Hello World!</h1>
      <Pool results={ results } />
      <Footer />
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    results: state.results,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(Actions, dispatch),
  };
}
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Index);
