import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch'
import Time from 'react-time'

// var scripts = document.getElementsByTagName("script");
// var thisUrl = scripts[scripts.length-1].src;
var thisUrl="http://localhost:5000/apply/static/bundle.js"

var classNames = require('classnames');

class Checklists extends React.Component {
  constructor(props) {
    super(props);
    this.state = {allSelected: false}
    this.checked = Array.apply(null, Array(this.props.school.checklists.length)).map(Boolean.prototype.valueOf, false);
  }
  selectAll() {
    this.state.allSelected = ! this.state.allSelected;
    if (this.state.allSelected) {
      this.checked.fill(true);
    } else {
      this.checked.fill(false);
    }
    this.setState({checked: this.checked});
  }
  checkBoxClicked(i) {
    if (this.checked[i]) {
      this.checked[i] = false;
    } else {
      this.checked[i] = true;
    }
    this.setState({checked: this.checked[i]});
  }
  classForRow(i) {
    return this.checked[i] ? "selected" : null;
  }
  render() {
    var contextualActionsClass = classNames({
      'contextual-actions': true,
      'active': this.checked.some(x => x)
    });
    return (
      <div>
        <div className={contextualActionsClass}>
          <button className="btn btn-default btn-sm"><input className="select-all" type="checkbox" onClick={() => this.selectAll()}/></button>&nbsp;
          <a className="btn btn-default" href="#">Accept Applications</a>&nbsp;
          <a className="btn btn-default" href="#">Delete Applications</a>
        </div>
        <table className="people-table table table-condensed table-hover">
          <thead>
            <tr>
              <th></th>
              <th>Child</th>
              <th>Parents</th>
              <th>Parent Observation</th>
              <th>Parent-Teacher Conversation</th>
              <th>Child Visit</th>
            </tr>
          </thead>
          <tbody>
            {
              this.props.school.checklists.map(
                function(checklist, i) {
                  checklist.checked = false;
                  return <tr key={checklist.id} className={this.classForRow(i)}>
                    <td>
                      <input key="select-one" type="checkbox" checked={this.checked[i]} className="select" onClick={() => this.checkBoxClicked(i)}/>
                    </td>
                    <td className="child">
                      {checklist.response.child.first_name} {checklist.response.child.last_name}<br/>
                      {checklist.response.child.dob}<br/>
                      {checklist.response.child.gender}
                    </td>
                    <td className="parents">
                      {checklist.response.parents[0].first_name} {checklist.response.parents[0].last_name}<br/>
                      <a href="mailto:{checklist.response.parents[0].email}">{checklist.response.parents[0].email}</a><br/>
                      {checklist.response.parents[0].phone}<br/>
                      { checklist.response.parents[1].first_name &&
                        <div>
                          <hr/>
                          {checklist.response.parents[1].first_name} {checklist.response.parents[1].last_name}<br/>
                          <a href="mailto:{checklist.response.parents[1].email}">{checklist.response.parents[1].email}</a><br/>
                          {checklist.response.parents[1].phone}<br/>
                        </div>
                      }
                    </td>
                    <td className="parent-observation">
                      { checklist.parent_observation_scheduled_at ?
                        <div className="scheduled_at">{ checklist.parent_observation_scheduled_at }</div>
                        :
                        <div>
                          <div className="unscheduled">Unscheduled</div>
                          { this.props.school.parent_observation_optional && '(optional)' }
                        </div>
                      }
                    </td>
                    <td className="parent-teacher-conversation">
                      { checklist.parent_teacher_conversation_scheduled_at ?
                        <div className="scheduled_at"><Time value={ checklist.parent_teacher_conversation_scheduled_at } format="ddd, MM/DD, h:mma"/></div>
                        :
                        <div>
                          <div className="unscheduled">Unscheduled</div>
                          { this.props.school.parent_conversation_optional && '(optional)' }
                        </div>
                      }
                    </td>
                    <td className="child-visit">
                      { checklist.visit_scheduled_at ?
                        <div className="scheduled_at">{ checklist.child_visit_scheduled_at }</div>
                        :
                        <div>
                          <div className="unscheduled">Unscheduled</div>
                          { this.props.school.child_visit_optional && '(optional)' }
                        </div>
                      }
                    </td>
                  </tr>
                }, this
              )
            }
          </tbody>
        </table>
      </div>
    )
  }
}

class School extends React.Component {
  constructor() {
    super();
    this.state = { school: null };
    var that = this;
    fetch(thisUrl + "/../../school/" + tc.env.currentSchoolId + "/" + tc.env.userApiToken)
      .then(function(response) {
        return response.json()
      }).then(function(json) {
        that.setState({
          school: json
        })
      }).catch(function(ex) {
        alert('parsing failed:' + ex)
      })
  }
  render() {
    return (
      <div>
        { this.state.school ?
          <div className="school">
            <h1 className><span className="page-title">Applications</span></h1>
            <Checklists school={this.state.school}/>
          </div>
          :
          <div className="loading">
            Loading...
          </div>
        }
      </div>
    );
  }
}

setTimeout(function(){
  if (location.pathname.endsWith('wf/admin/applications')) {
    document.title = 'Applications';
    ReactDOM.render(
      <School />,
      document.getElementById('foundation')
    );
  }
}, 200);
