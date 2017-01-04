import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch'
import Time from 'react-time'

class Checklists extends React.Component {
  constructor(props) {
    super(props);
    this.checked = Array.apply(null, Array(this.props.school.checklists.length)).map(Boolean.prototype.valueOf, false);
  }
  checkBoxClicked(i) {
    if (this.checked[i]) {
      this.checked[i] = false;
    } else {
      this.checked[i] = true;
    }
    this.forceUpdate();
  }
  rowClass(i) {
    if (this.checked[i] == true) {
      return "selected";
    } else {
      return null;
    }
  }
  render() {
    return (
      <div>
        <table className="people-table table table-condensed table-hover">
          <thead>
            <tr>
              <th></th>
              <th>Child</th>
              <th>Parents</th>
              <th>Observation</th>
              <th>Interview</th>
              <th>Visit</th>
            </tr>
          </thead>
          <tbody>
            {
              this.props.school.checklists.map(
                function(checklist, i) {
                  checklist.checked = false;
                  return <tr key={checklist.id} className={this.rowClass(i)}>
                    <td>
                      <input type="checkbox" className="select" onClick={() => this.checkBoxClicked(i)}/>
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
                      {checklist.response.parents[0].address.split("\n").map(function (item, i, arr) { return <span key={i}>{item}{ arr.length-1 === i ? null : <br/>}</span> }) }
                      { checklist.response.parents[1].first_name &&
                        <div>
                          <hr/>
                          {checklist.response.parents[1].first_name} {checklist.response.parents[1].last_name}<br/>
                          <a href="mailto:{checklist.response.parents[1].email}">{checklist.response.parents[1].email}</a><br/>
                          {checklist.response.parents[1].phone}<br/>
                          {checklist.response.parents[1].address.split("\n").map(function (item, i, arr) { return <span key={i}>{item}{ arr.length-1 === i ? null : <br/>}</span> }) }
                        </div>
                      }
                    </td>
                    <td className="observation">
                      { checklist.observation_scheduled_at ?
                        <div className="scheduled_at">{ checklist.observation_scheduled_at }</div>
                        :
                        <div>
                          <div className="unscheduled">Unscheduled</div>
                          { this.props.school.observation_optional && '(optional)' }
                        </div>
                      }
                    </td>
                    <td className="interview">
                      { checklist.interview_scheduled_at ?
                        <div className="scheduled_at"><Time value={ checklist.interview_scheduled_at } format="ddd, MM/DD, h:mma"/></div>
                        :
                        <div>
                          <div className="unscheduled">Unscheduled</div>
                          { this.props.school.interview_optional && '(optional)' }
                        </div>
                      }
                    </td>
                    <td className="visit">
                      { checklist.visit_scheduled_at ?
                        <div className="scheduled_at">{ checklist.visit_scheduled_at }</div>
                        :
                        <div>
                          <div className="unscheduled">Unscheduled</div>
                          { this.props.school.visit_optional && '(optional)' }
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
    fetch('http://localhost:5000/apply/school/1')
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
            <h1 className><span className="page-title">{this.state.school.name} Applications</span></h1>
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
