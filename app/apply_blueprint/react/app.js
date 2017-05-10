// http://localhost:3000/s/2/networks/wf/application/parent_email

import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch'

var scripts = document.getElementsByTagName("script");
var thisUrl = scripts[scripts.length-1].src;


class UI extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: "" };
    var that = this;
    fetch(thisUrl + "/../../email_template?tc_school_id=" + tc.env.currentSchoolId + "&tc_api_token=" + tc.env.userApiToken)
      .then(function(response) {
        return response.text()
      }).then(function(text) {
        that.setState({value: text});
      }).catch(function(ex) {
        alert('failed:' + ex);
      })
  }
  changed(e) {
    this.setState({value: e.target.value});
  }
  save(e) {
    var that = this;
    fetch(thisUrl + "/../../email_template_post_parameters?tc_school_id=" + tc.env.currentSchoolId + "&tc_api_token=" + tc.env.userApiToken)
      .then(function(response) {
        return response.json()
      }).then(function(json) {

        var f  = new FormData();
        for (var k in json.fields) {
          f.append(k, json.fields[k]);
        }

        var b = new Blob([that.state.value], {type: "text/html"});
        f.append("file", b);

        // "https://requestb.in/pcfczlpc"
        // json.url
        fetch(json.url , {
           method: 'POST',
          //  'Content-type', 'multipart/form-data'
          //  headers: {'Content-Type': 'application/json'},
           body: f
         }).then(function(response) {

         }).catch(function(ex) {
           alert('updating status failed:' + ex);
         })

      }).catch(function(ex) {
        alert('failed:' + ex);
      })

    // change button to say saving, then saved, then back to save
    // change colors of button to make it obvious
  }
  render() {
    return (
      <div>
        <b>Parent Email Template</b><br/>
        <textarea name="template" id="template" cols="120" rows="20" value={this.state.value} onChange={(e) => this.changed(e)}></textarea><br/>
        <input type="button" value="Save" onClick={(e) => this.save(e)}/><br/>
      </div>
    )
  }
}

setTimeout(function(){
  if (location.pathname.endsWith('application/parent_email')) {
    document.title = 'Parent Email Template';
    ReactDOM.render(
      <UI />,
      document.getElementById('foundation')
    );
  }
}, 200);
