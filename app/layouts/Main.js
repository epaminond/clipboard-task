import React, { Component, PropTypes } from 'react';
import Helmet from 'react-helmet';

class Main extends Component {

  componentWillMount() {
    window.scrollTo(0, 0);
  }

  render() {
    return (
      <div>
        <Helmet titleTemplate="%s | Clipboard Health" defaultTitle="Clipboard Health" />
        <div id="main">
          {this.props.children}
        </div>
      </div>);
  }

}

Main.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]),
};

Main.defaultProps = {
  children: null,
};

export default Main;
