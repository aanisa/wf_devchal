// http://localhost:3000/s/2/networks/wf/application/parent_email

import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch'

var scripts = document.getElementsByTagName("script");
var thisUrl = scripts[scripts.length-1].src;

class UI extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: "", label: "Save", disabled: false};
    var that = this;
    fetch(thisUrl + "/../../email_template?tc_school_id=" + tc.env.currentSchoolId)
      .then(function(response) {
        if (response.status == 404) {
          fetch(thisUrl + "/../../email_template?tc_api_token=" + tc.env.userApiToken)
            .then(function(response) {
              return response.text();
            }).then(function(text) {
              that.setState({value: text});
            }).catch(function(ex) {
              alert('failed:' + ex);
            })
        } else {
          return response.text();
        }
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
    this.setState({label: "Saving...", disabled: true})
    var that = this;
    // console.warn('XHR ISSUE',xhr.responseText);
    fetch(thisUrl + "/../../email_template_post_parameters?tc_school_id=" + tc.env.currentSchoolId + "&tc_api_token=" + tc.env.userApiToken)
      .then(function(response) {
        console.log('Response', response.json());
        // In Response.json() --> [[PromiseValue]] :SyntaxError: Unexpected token < in JSON at position ]
        //unable to save
        return response.json();
      }).then(function(json) {
        var f  = new FormData();
        for (var k in json.fields) {
          f.append(k, json.fields[k]);
        }
        var b = new Blob([that.state.value], {type: "text/html"});
        f.append("file", b);
        fetch(json.url , {
           method: 'POST',
           body: f
         }).then(function(response) {
           that.setState({label: "Saved"})
           setTimeout(function() {
             that.setState({label: "Save", disabled: false})
           }, 3000)
         }).catch(function(ex) {
           alert('updating status failed:' + ex);
         })
      }).catch(function(ex) {
        alert('failed:' + ex);
      })
  }
  keyDown(e) {
    if (e.metaKey && e.keyCode == 83) {
      this.save(e);
      e.preventDefault();
      return false;
    }
  }
  textEdit() {
    console.log('Add some Text');
    
  }

  render() {
    return (
      <div>
        <b>Parent Email Template</b><br/>
        <div>
          <div name="textEditor">
            <button onClick={this.textEdit}>Add Text</button>
          </div>
          <div >
            <textarea name="template" id="template" cols="120" rows="20" value={this.state.value} onChange={(e) => this.changed(e)} onKeyDown={(e) => this.keyDown(e)}></textarea><br/>
            <input type="button" value={this.state.label} onClick={(e) => this.save(e)} disabled={this.state.disabled}/><br/>
          </div>
        </div>
      </div>
    )
  }
}

setTimeout(function(){
  if (location.pathname.endsWith('application/parent_email_template')) {
    document.title = 'Application: Parent Email Template';
    ReactDOM.render(
      <UI />,
      document.getElementById('foundation')
    );
  }

  if (location.pathname == '/s/' + tc.env.currentSchoolId + '/schools/' + tc.env.currentSchoolId) {
    var div = document.createElement("div");
    div.innerHTML = '<a href="/s/' + tc.env.currentSchoolId + '/networks/wf/application/parent_email_template">Online Application: Parent Email Template</a>'
    var form = document.querySelector('#edit_school')
    form.parentNode.insertBefore(div, form.nextSibling);
  }

}, 200);
