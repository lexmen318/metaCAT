import axios from 'axios'

let API_LINK_BASE = ''

var backend = {
  data () {
    return {
      uploadBatchUrl: API_LINK_BASE + `/upload_batch_allocation`
    }
  },
  methods: {
    /********************************
    * LOGIN FUNCTIONS
    ********************************/
    async login (login_name, password) {
      const apiLink = API_LINK_BASE + '/auth/login'
      try {
        let response = await axios.post(apiLink, {login_name: login_name, password: password})
        return response.data
      } catch (error) {
        console.log(error)
      }
    },
    async logout () {
      const apiLink = API_LINK_BASE + '/auth/logout'
      try {
        let response = await axios.post(apiLink)
        return response.data
      } catch (error) {
        console.log(error)
      }
    },
    async register (loginName, userName, password) {
      const apiLink = API_LINK_BASE + '/auth/register'
      try {
        let response = await axios.post(apiLink, {login_name: loginName, user_name: userName, password: password})
        return response.data
      } catch (error) {
        console.log(error)
      }
		},
		async change_language (languageCode) {
      const apiLink = API_LINK_BASE + '/language/' + languageCode
      try {
        let response = await axios.get(apiLink)
        return response.data
      } catch (error) {
        console.log(error)
      }
    },
    /********************************
    * FILE NAME FUNCTIONS
    ********************************/
    async batch_list_by_category (batch_category) {
      const apiLink = API_LINK_BASE + `/batch_list_by_category?batch_category=${batch_category}`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async batch_description_post (batch_id, batch_description, batch_category) {
      const apiLink = API_LINK_BASE + '/batch_description_post'
      try {
        let param = {
          batch_id: batch_id,
          batch_description: batch_description,
          batch_category: batch_category
        }
        let response = await axios.post(apiLink, param)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async get_name (batch_id) {
      let dialogues = {}
      const apiLink = API_LINK_BASE + '/name'
      try {
        let response = await axios.get(apiLink)
        console.log('=============File Name==============')
        console.log(response.data.name)
        return response.data.name
      } catch (error) {
        console.log(error)
      }
    },
    async put_name (name) {
      let dialogues = {}
      const apiLink = API_LINK_BASE + '/name'
      try {
        let response = await axios.put(apiLink, {name: name})
        return true
      } catch (error) {
        console.log(error)
        return false
      }
    },
    /********************************
    * API INTERACTION FUNCTIONS
    ********************************/
    async annotating_turns (query, domains) {
      let params = {
        query: query,
        domains: domains
      }
      const apiLink = API_LINK_BASE + '/annotating/turns'
      try {
        let response = await axios.post(apiLink, params)
        return response.data
      } catch (error) {
        console.log(error)
      }
    },
    /***************************************
    * DIALOGUES METADATA RESOURCE
    ***************************************/
    async annotating_dialogues_metadata (batch_id) {
      let dialogues = {}
      const apiLink = API_LINK_BASE + '/annotating/dialogues_metadata/' + batch_id
      try {
        let response = await axios.get(apiLink)
        let dialoguesList = response.data
        return dialoguesList
      } catch (error) {
        console.log(error)
        alert("Couldn't connect to server, check that it's running.")
      }
    },
    async change_dialogue_name_async (oldName, newName) {
      const apiLink = API_LINK_BASE + `/annotating/dialogues_metadata/${oldName}`
      try {
        let response = await axios.put(apiLink, {id: newName})
        console.log('---- RESPONSE TO NAME CHANGE ----', response)
        return true
      } catch (error) {
        console.log(error)
      }
      return false
    },
    /***************************************
    * DIALOGUES RESOURCE
    ***************************************/
    async get_all_dialogues_async () {
      let dialogues = {}
      try {
        let response = await this.RESTdialogues('GET', null, {})
        dialogues = response.data
        return dialogues
      } catch(error) {
        console.log(error)
      }
    },
    async validate_turn (batch_id, dialogue_id, turn_id, metadata_name, turn) {
      let param = {
        turn: turn[0],
        metadata_name: metadata_name
      }
      let url = `/annotating/validate_turn/${batch_id}/${dialogue_id}/${turn_id}`
      try {
        let response = await axios.put(url, param)
        return response.data
      } catch(error) {
        console.log(error)
      }
    },
    async validate_dialogue (batch_id, dialogue_id, metadata_name, turn_list) {
      let param = {
        turn_list: turn_list,
        metadata_name: metadata_name
      }
      let url = `/annotating/validate_dialogues/${batch_id}/${dialogue_id}`
      try {
        let response = await axios.put(url, param)
        return response.data
      } catch(error) {
        console.log(error)
      }
    },
    async get_all_dialogues_async_multiwoz () {
      let dialogues = {}
      try {
        let response = await this.RESTdialogues('GET', 'MultiWOZ', {})
        dialogues = response.data
        return dialogues
      } catch (error) {
        console.log(error)
      }
    },
    async get_single_dialogue_async (batch_id, id) {
      try {
        let response = await this.RESTdialogues('GET', batch_id, id, {})
        console.log('===== GOT SINGLE DIALOGUE =====')
        console.log(response)
        let dialogue = response.data
        // let dialogue = response.data.dialogue
        return dialogue
      } catch (error) {
        console.log(error)
      }
    },
    async post_empty_dialogue (batchId) {
      try {
        const response = await this.RESTdialogues('POST', batchId, null, null)
        console.log(response)
        return response.data.id
      } catch (error) {
        console.log(error)
      }
    },
    async post_new_dialogues_from_string_lists_async (stringLists) {
      try {
        const response = await this.RESTdialogues('POST', batchId, null, stringLists)
        console.log('RECEIVED RESPONSE TO POST DATA')
        console.log(response)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async post_new_dialogue_from_json_string_async (jsonString) {
      try {
        const response = await this.RESTdialogues('POST', batchId, null, JSON.parse(jsonString))
        console.log('RECEIVED RESPONSE TO POST DATA')
        console.log(response)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async put_single_dialogue_async (batchId, dialogueId, dTurns) {
      try {
        const response = await this.RESTdialogues('PUT', batchId, dialogueId, dTurns)
        console.log('---- RESPONSE TO PUT ----', response)
        var status = response.data.status
        console.log('status', status)
        return status
      } catch (error) {
        console.log(error)
      }
    },
    async del_single_dialogue_async (batchId, dialogueId) {
      try {
        const response = await this.RESTdialogues('DELETE', batchId, dialogueId)
        console.log('---- RESPONSE TO DEL ----', response)
      } catch (error) {
        console.log(error)
      }
    },
    async RESTdialogues (method, batchId, id, params) {
      console.log('********** ACCESSING DIALOGUES RESOURCE **********')
      console.log('ID: ' + id)
      console.log('METHOD' + method)
      console.log('PARAMS' + params)
      var apiLink
      if (id == null) {
        apiLink = API_LINK_BASE + `/annotating/dialogues_main/${batchId}`
      } else {
        apiLink = API_LINK_BASE + `/annotating/dialogues_detail/${batchId}/${id}`
      }

      var response
      if (method === 'DELETE') {
        response = await axios.delete(apiLink)
      } else if (method === 'PUT') {
        response = await axios.put(apiLink, params)
      } else if (method === 'POST') {
        response = await axios.post(apiLink, params)
      } else if (method === 'GET') {
        response = await axios.get(apiLink, params)
      } else {
        console.log('********** INVALID METHOD **********')
      }
      console.log(response)
      return response
    },
    async annotating_dialogue_status (batch_id, dialogue_id, currentStatus) {
      const apiLink = API_LINK_BASE + `/annotating/dialogue_status`
      try {
        let response = await axios.post(apiLink, {batch_id: batch_id, dialogue_id: dialogue_id, currentStatus: currentStatus})
        console.log('---- RESPONSE TO NAME CHANGE ----', response)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    /***************************************
    * BATCH ALLOCATION
    ***************************************/
    async user_list (file) {
      const apiLink = API_LINK_BASE + `/data_mgmt/user_list`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
		},
		async upload_metadata (file) {
      const apiLink = API_LINK_BASE + `/data_mgmt/upload_metadata`
      try {
        let response = await axios.post(apiLink, {batch_file: file})
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async upload_batch_allocation (file) {
      const apiLink = API_LINK_BASE + `/data_mgmt/upload_batch_allocation`
      try {
        let response = await axios.post(apiLink, {batch_file: file})
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async batch_allocation_list (type) {
      const apiLink = API_LINK_BASE + `/data_mgmt/batch_allocation_list?batch_category=${type}`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async batch_allocation (batch_id_list, allocate_login_name, batch_category) {
      const apiLink = API_LINK_BASE + `/data_mgmt/batch_allocation`
      try {
        let param = {
          batch_id_list: batch_id_list,
          allocate_login_name: allocate_login_name,
          batch_category: batch_category
        }
        let response = await axios.post(apiLink, param)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async error_file_list () {
      const apiLink = API_LINK_BASE + `/sys_mgmt/error_file_list`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async remove_error (errorKey) {
      const apiLink = API_LINK_BASE + `/sys_mgmt/remove_error/` + errorKey
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async sys_init () {
      const apiLink = API_LINK_BASE + `/sys_mgmt/sys_init`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
		},
		async metadata () {
      const apiLink = API_LINK_BASE + `/data_mgmt/metadata`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
		},
		async metadata_detail (category, metadata_name) {
      const apiLink = API_LINK_BASE + `/data_mgmt/metadata/${category}/${metadata_name}`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    // async get_all_paraphrasing_dialogues (batch_id, dialogues_id) {
    //   const apiLink = API_LINK_BASE + `/paraphrasing/dialogues/${batch_id}/${dialogues_id}`
    //   try {
    //     let response = await axios.get(apiLink)
    //     return response
    //   } catch (error) {
    //     console.log(error)
    //   }
    // },
    async delete_paraphrasing_dialogues (batch_id, dialogues_id) {
      let apiLink = API_LINK_BASE + `/paraphrasing/dialogues_detail/${batch_id}/${dialogues_id}`
      try {
        let response = await axios.delete(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async get_paraphrasing_dialogues (batch_id, dialogues_id) {
      let apiLink = ''
      if (dialogues_id) {
        apiLink = API_LINK_BASE + `/paraphrasing/dialogues_detail/${batch_id}/${dialogues_id}`
      } else {
        apiLink = API_LINK_BASE + `/paraphrasing/dialogues_main/${batch_id}`
      }
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async updata_paraphrasing_dialogues (batch_id, dialogues_id, turn_list) {
      const apiLink = API_LINK_BASE + `/paraphrasing/dialogues_detail/${batch_id}/${dialogues_id}`
      try {
        let response = await axios.put(apiLink, turn_list)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async validate_paraphrasing_dialogues (batch_id, dialogues_id, turn_list) {
      const apiLink = API_LINK_BASE + `/paraphrasing/validate_dialogues/${batch_id}/${dialogues_id}`
      try {
        let response = await axios.put(apiLink, turn_list)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async validate_paraphrasing_turn (batch_id, dialogues_id, turn) {
			let turn_id = Object.keys(turn)[0]
			let para_dialogue = turn[turn_id]
      const apiLink = API_LINK_BASE + `/paraphrasing/validate_turn/${batch_id}/${dialogues_id}/${turn_id}`
      try {
        let response = await axios.put(apiLink, para_dialogue)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async data_convert_operations () {
      const apiLink = API_LINK_BASE + `/sys_admin/data_convert_operations`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
		},
		async getProgressData () {
      const apiLink = API_LINK_BASE + `/sys_progress/list`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async getSysSettingView () {
      const apiLink = API_LINK_BASE + `/sys_setting/view`
      try {
        let response = await axios.get(apiLink)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async sysSettingChange (annotating, paraphrasing) {
      const apiLink = API_LINK_BASE + `/sys_setting/change`
      try {
        let param = {
          config:{
             annotating: annotating,
             paraphrasing: paraphrasing
          }
        }
        let response = await axios.post(apiLink, param)
        return response
      } catch (error) {
        console.log(error)
      }
    },
    async changeAdminPwd (adminForm) {
      const apiLink = API_LINK_BASE + `/auth/change_admin_pwd`
      try {
        let param = {
					oldPassWord: adminForm.oldPassWord,
					password: adminForm.passWord,
          confirmPassWord: adminForm.confirmPassWord
        }
        let response = await axios.post(apiLink, param)
        return response
      } catch (error) {
        console.log(error)
      }
    }

  }
}

export default backend
