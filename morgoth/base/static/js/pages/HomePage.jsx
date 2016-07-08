import React from 'react';

import Paper from 'material-ui/Paper';
import ActionExtension from 'material-ui/svg-icons/action/extension';
import NavigationApps from 'material-ui/svg-icons/navigation/apps';

import HomeMenu from '../components/HomeMenu.jsx';


const MENU_ITEMS = [
  {
    text: 'Addons',
    linkTo: '/addons/',
    icon: <ActionExtension />
  },
  {
    text: 'Addon Groups',
    linkTo: '/addons_groups/',
    icon: <NavigationApps />
  }
];

class HomePage extends React.Component {
  render() {
    return (
      <Paper zDepth={2}>
        <HomeMenu items={MENU_ITEMS} />
      </Paper>
    )
  }
}

export default HomePage;
