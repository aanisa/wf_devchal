import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch'

class Checklists extends React.Component {
  render() {
    return (
      <div>
        {
          this.props.school.checklists.map(
            function(checklist) {
              return <div key={checklist.id}>
                <div className="child">
                  {checklist.response.child.first_name} {checklist.response.child.last_name}<br/>
                  {checklist.response.child.dob}
                </div>
                <div className="parent">
                  {checklist.response.parents[0].first_name} {checklist.response.parents[0].last_name}<br/>
                  <a href="mailto:{checklist.response.parents[0].email}">{checklist.response.parents[0].email}</a><br/>
                  {checklist.response.parents[0].phone}<br/>
                  {checklist.response.parents[0].address}<br/>
                </div>
                <div className="parent">
                  {checklist.response.parents[1].first_name} {checklist.response.parents[1].last_name}<br/>
                  <a href="mailto:{checklist.response.parents[1].email}">{checklist.response.parents[1].email}</a><br/>
                  {checklist.response.parents[1].phone}<br/>
                  {checklist.response.parents[1].address}<br/>
                </div>
                <div className="observation">
                  observation:
                  { checklist.observation_scheduled_at ?
                    <div className="scheduled_at">{ checklist.observation_scheduled_at }</div>
                    :
                    <div className="unscheduled">unscheduled</div>
                  }
                  { this.props.school.observation_optional && '(optional)' }
                </div>
                <div className="interview">
                  interview:
                  { checklist.interview_scheduled_at ?
                    <div className="scheduled_at">{ checklist.interview_scheduled_at }</div>
                    :
                    <div className="unscheduled">unscheduled</div>
                  }
                  { this.props.school.interview_optional && '(optional)' }
                </div>
                <div className="visit">
                  visit:
                  { checklist.visit_scheduled_at ?
                    <div className="scheduled_at">{ checklist.visit_scheduled_at }</div>
                    :
                    <div className="unscheduled">unscheduled</div>
                  }
                  { this.props.school.visit_optional && '(optional)' }
                </div>
              </div>
            }, this
          )
        }
      </div>
    )
  }
}

class School extends React.Component {
  constructor() {
    super();
    var that = this;
    fetch('../school/1')
      .then(function(response) {
        return response.json()
      }).then(function(json) {
        that.setState({
          school: json
        })
      }).catch(function(ex) {
        alert('parsing failed:' + ex)
      })

    this.state = {
      school: null
    }
  }
  render() {
    return (
      <div>
      { this.state.school ?
          <div className="school">
            {this.state.school.name}
            <Checklists checklists={this.state.school.checklists} school={this.state.school}/>
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

ReactDOM.render(
  <School />,
  document.getElementById('root')
);
