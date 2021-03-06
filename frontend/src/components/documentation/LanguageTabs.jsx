import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';


/*
  This Component is the top nav bar which also controls the language of
  the code examples.

  It passes the selected language to all of its children
*/

export default class LanguageTabs extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      activeLanguage: "python"
    }

    this.changeActiveLanguage = this.changeActiveLanguage.bind(this);
    this.renderChildren = this.renderChildren.bind(this);
  }

  changeActiveLanguage(language) {
    this.setState({activeLanguage: language})
  }

  renderChildren(props) {
    return React.Children.map(props.children, (child, i) => {
      return React.cloneElement(child, {
        activeLanguage: this.state.activeLanguage
      })
    })
  }

  render() {
    return (
      <div>
        <div className="tab">
          <div className="row">
            <div className="col">

            </div>
            <div className="col">
              <Tabs
                value={this.state.activeLanguage}
                onChange={this.changeActiveLanguage}>
                <Tab
                  label="Python"
                  value="python">
                </Tab>
                <Tab
                  label="JavaScript"
                  value="javascript">
                </Tab>
                <Tab
                  label="Shell"
                  value="shell">
                </Tab>
              </Tabs>
            </div>
          </div>
        </div>

        <div className="main">
          {this.renderChildren(this.props)}
        </div>
      </div>
    );
  }

}
