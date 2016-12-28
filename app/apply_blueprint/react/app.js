import React from 'react';
import ReactDOM from 'react-dom';

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
    this.state = {
      school: {
        "checklists": [
          {
            "date_created": "2016-12-15T14:52:45.797630+00:00",
            "date_modified": "2016-12-15T14:52:45.797630+00:00",
            "guid": "1234",
            "id": 1,
            "interview_scheduled_at": null,
            "observation_scheduled_at": null,
            "response": {
              "child": {
                "dob": "05/31/2006",
                "first_name": "Kid",
                "last_name": "Oh"
              },
              "guid": "1234",
              "parents": [
                {
                  "address": "8513 172nd St. W\r\nLakeville, MN 55044",
                  "email": "dan.grigsby@wildflowerschools.org",
                  "first_name": "Dan",
                  "last_name": "Grigsby",
                  "phone": "612-423-3694"
                },
                {
                  "address": null,
                  "email": null,
                  "first_name": null,
                  "last_name": null,
                  "phone": null
                }
              ]
            },
            "school": 1,
            "visit_scheduled_at": null
          }
        ],
        "date_created": "2016-12-15T14:52:45.797630+00:00",
        "date_modified": "2016-12-15T14:52:45.797630+00:00",
        "email": "mail@example.com",
        "id": 1,
        "interview_optional": false,
        "match": "aster",
        "name": "Aster Montessori School",
        "observation_optional": false,
        "schedule_interview_url": "http://TBD",
        "schedule_observation_url": "http://TBD",
        "schedule_visit_url": "http://TBD",
        "visit_optional": false
      }
    }
  }
  render() {
    return (
      <div className="school">
        {this.state.school.name}
        <Checklists checklists={this.state.school.checklists} school={this.state.school}/>
      </div>
    );
  }
}

ReactDOM.render(
  <School />,
  document.getElementById('root')
);
