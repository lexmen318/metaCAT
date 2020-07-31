export default {
	lang: {
		targetLanguageName: '中文',
		languageEnCode: 'en',
		languageEnName: 'English',
		languageCnCode: 'cn',
		languageCnName: 'Chinese',
	},
	topMenu: {
		helpTitle: 'Help',
		welcomeTitle: 'Welcome,',
		logoutTitle: 'Logout',
		annotatingTitle: 'Annotating',
		paraphrasingTitle: 'Paraphrasing',
	},
	general: {
		lblReminder: 'Reminder',
		btnClose: 'Close',
		btnCancel: 'Cancel',
		btnConfirm: 'Confirm',
		btnOK: 'OK',
		btnYes: 'Yes',
		btnNo: 'No'
	},
	message: {
		hello: '{msg} metaCAT'
	},
	alert: {
		lblHint: 'Hint',
		lblCustomizeComponent: 'Customize Popup Component',
		lblSelectBatch: 'Select allocation batch please.',
		lblSelectUser: 'Select allocation user please.',
		lblOnlyJsonAllowed: 'Only json supportted.',
		lblOnlyZipAllowed: 'Only zip supportted.',
		lblAllocateWarning: 'If unallocated files exists, will be covered. Continue?',
		lblConfirmToRun: 'Confirm to execute?',
		lblOperationSuccess: 'Operation successful',
		lblSettingSuccess: 'Setting successful',
		lblJsonFormatError: 'Json format error. Server error:',
		lblTxtJsonOnlySupport: 'Only txt/json supported.',
		lblConfirmToDeleteTurn: 'Confirm to delete current turn?',
		lblAbandonChange: 'Abandon change',
		lblSaveChange: 'Save change',
		lblReturnAbandonChange: 'Confirm to save change, or directly return.',
		lblErrorNotSaved: 'Dialogue not saved, server error happened.'
	},
	login: {
		appTitle: 'metaCAT--Integrated Annotation Platform for Dialogue Data',
		appDesc: 'metaCAT is an integrated platform built for intelligent Q&A and chatbot aiming at metadata modeling, data annotating, and model testing. It supports the training and testing of dialogue and Q&A models by implementing core functions such as collaborated annotating, rule-based automatic annotating, and model interactive testing.',
		btnLogin: 'Login',
		btnRegister: 'Register',
		btnCancel: 'Cancel',
		registrationHint: 'No account?',
		loginNameHolder: 'Login Name',
		loginNameHint: 'Please input login name',
		userNameHolder: 'User Name',
		userNameHint: 'Please input user name',
		passWordHolder: 'Password',
		passWordHint: 'Please input password',
		confirmPassWordHolder: 'Confirm Password',
		confirmPassWordHint: 'Please confirm password',
	},
	adminMenu: {
		menuTitle: 'System Maintenance',
		tabTaskProgress: 'Task Progress',
		tabDataMgmt: 'Data Management',
		tabSysMgmt: 'System Operation',
		tabSysSetting: 'System Setting',
	},
	taskProgress: {
		tabTitle: 'Task Progress',
		number: 'No.',
		userName: 'User Name',
		batch: 'Batch No.',
		metadataCategory: 'Metadata Category',
		metadataName: 'Metadata Name',
		progress: 'Task Progress',
		description: 'Description'
	},
	dataMgmt: {
		datasetMetadata: 'Dataset Metadata',
		number: 'No.',
		metadataCategory: 'Metadata Category',
		metadataName: 'Metadata Name',
		operation: 'Operation',
		view: 'View',

		metadata: 'Metadata ',
		metadataDesc: 'is a segment of data used to describe the dialogue domain, intention, and slot annotation system.  It is stored in JSON format and determines the optional service domains on the user side and system side, slots in each service domain, valid slot-values in each slot, and allowed intents.',
		metadataGeneral: 'General: ',
		metadataGeneralDesc: 'This type of domain contains only some intent without actual slots, such as "Thank" and "Bye", etc.',
		metadataDomain: 'Service Domain: ',
		metadataDomainDesc: 'These types of domain contain some specific intents with slots, e.g. "Hotel" and "Restaurant". Generally, a dialogue involves one service domain. However, in a few cases, it may involve two service domains, e.g. "Hotel" and "Taxi". ',
		metadataIntent: 'Intent: ',
		metadataIntentDesc: 'It represents the intent expressed in each utterance. It is possible that one utterance contains multiple intents.',
		metadataSlot: 'Slot: ',
		metadataSlotDesc: 'It indicates the key information carried by the intent. Non-enumerated slots are usually one word or short segment of text taken from the original utterance text. Enumerated slots only have some specific slot-values and may not appear in the utterance text of the dialogue.',

		batchDivider: 'Batch Assigning',
		userAllocate: 'User Name',
		userAllocateHint: 'Please select user to assign',
		batchAllocate: 'Assign Batch',
		annotating: {
			title: 'Annotating',
			number: 'No.',
			batchNo: 'Batch No',
			metadataName: 'Metadata Name',
		},
		paraphrasing: {
			title: 'Paraphrasing',
			number: 'No.',
			batchNo: 'Batch No.',
			metadataName: 'Metadata Name',
		}
	},
  sysMgmt: {
		lblInit: 'Initialization',
		btnInit: 'Initialize Directory',
		lblMetadata: 'Metadata',
		btnImportMetadata: 'Metadata Importing',
		lblBatchImporting: 'Batch Importing',
		btnUploadJsonBatch: 'Upload JSON Batch',
		btnUploadRawBatch: 'Upload RAW Batch',
		lblBatchExporting: 'Batch Exporting',
		btnDownloadAnnotatingBatch: 'Download Annotating Batch',
		btnDownloadMultiwozBatch: 'Download MultiWOZ Batch',
		btnDownloadParaphrasingBatch: 'Download Paraphrasing Batch',
		lblDataConverting: 'Data Converting',
		btnUpgradeDataVersion: 'Upgrade Data Version',
		btnDetectDataIntegrity: 'Detect Data Integrity',
		btnConvertSlotRealValue: 'Convert Slot Real Value',
		lblDataCleaning: 'Data Cleaning',
		btnCleanAnnotatingData: 'Clean Annotating Data',
		btnCleanParaphrasingData: 'Clean Paraphrasing Data',
		lblOperationErrorRecord: 'Operation Error Record',
		tblIndex: 'No.',
		tblErrorNo: 'Error No',
		tblErrorType: 'Error Type',
		tblErrorTime: 'Error Time',
		tblErrorDetail: 'Error Detail',
		tblErrorFile: 'Error File',
		tblDownload: 'Download',
		tblOperation: 'Operation',
		tblDelete: 'Delete',
		tblNoData: 'No Data',
	},
	sysSetting: {
		adminForm: {
			title: 'Admin PWD Changing',
			oldPassWord: 'Old PassWord',
			oldPassWordHolder: 'Please input old passWord',
			passWord: 'Password',
			passWordHolder: 'Please input new password',
			confirmPassWord: 'Confirm PassWord',
			confirmPassWordHolder: 'Please input confirming passWord',
			submitChangePwd: 'Change PassWord',
		},
		settingForm: {
			title: 'System Switch',
			annotatingTitle: 'Annotating:',
			annotating: {
				sysAnnotating: 'SYS Side Annotating',
				turnDeleteFlag: 'Dialogue Turn Deleting',
				turnAddFlag: 'Dialogue Turn Creating',
			},
			paraphrasingTitle: 'Paraphrasing:',
			paraphrasing: {
				asrOption: 'ASR Input',
				submitSysSetting: 'Submit',
				resetSysSetting: 'Reset'
			}
		}
	},
	annotatingFunction: {
		batch: {
			lblNoDataHint: 'No assigned task, please contact administrator.',
			lblChangeDescription: 'Change Description',
		},
		main: {
			counterHint: 'Drag file here to upload!',
			counterHeader: ' items totally',
			counterTail: ' items finished',
			btnCreateNewDialogue: 'Create New Dialogue',
			lblStatusFinished: ' Finished',
			lblStatusProcessing: ' Processing',
			lblDeleteHint: 'Hint',
			lblDeleteWarning: 'Confirm to delete? It is not recoverable!',
			btnDeleteDialogue: 'Delete',
			lblVisited: ' Visited',
			lblTurn: ' turns',
			msgNameChanged: 'Name Changed',
			msgNameChangedError: 'Server Error! Name Unchanged.',
			msgJsonFormatError: 'Wrong JSON format! Server Error:',
			msgTxtJsonOnlySupport: 'Only TXT/JSON formats are supported.'
		},
		detail: {
			lblCurrentTurn: 'Current Turn:',
			btnDialogueList: 'Back',
			btnTagValidate: 'Validate',
			lblChangeSaved: 'All Changes Saved',
			lblChangeNotSaved: 'Changes Unsaved',
			btnSave: 'Save',
			lblDialogueTurn: 'Turn:',
			lblNewTurnText: 'Please input user\'s utterance',
			lblNewTurnTitle: 'Please input user\'s utterance for new dialogue turn.',
			btnNewTurn: 'Send',
			lblTurnInputHint: 'Please input or paste',
			placeholderSlotValue: 'Slot value',
			placeholderSlotPosition: 'Position',
			placeholderSlotIntent: 'For intent'
		}
	},
	paraphrasingFunction: {
		batch: {
			lblNoDataHint: 'No assigned task, please contact administrator.',
			lblChangeDescription: 'Change Description',
		},
		main: {
			counterHeader: ' items totally',
			counterTail: ' items finished',
			lblDeleteHint: 'Hint',
			lblDeleteWarning: 'Confirm to delete? It is not recoverable!',
			btnDeleteDialogue: 'Delete',
			lblVisited: ' Visited',
			lblStatusFinished: ' Finished',
			lblTurn: ' turns',
		},
		detail: {
			lblDialogueId: 'Dialogue ID：',
			lblDomainSeries: 'Domain Sequence',
			lblStandardSlot: 'Standard Dialogue Slots',
			lblparaphrasingSlot: 'Paraphrased Dialogue Slots',
			btnTaskDescription: 'Task Description',
			btnValidate: 'Validate',
			btnSave: 'Save',
			btnBackToMain: 'Back',
			lblTaskHint: 'Please use colloquial language to paraphrase the utterance, introducing as many diversity as possible. After the paraphrasing, some slots should be annotated by drag-and-drop operation to complete the annotation.',
			lblDialogueTurn: 'Turn:',
			lblTurnUser: 'USR',
			lblTurnSys: 'SYS',
			lblStandardDialogue: 'Standard',
			lblparaphrasingDialogue: 'Paraphrased',
			lblparaphrasingDialogueHint: 'Please input utterance text to paraphrase',
			lblAsrNoDataHint: 'No content recognized from ASR input',
			lblScenarioDescription: 'Task Scenario Description',
			lblSlotLabel: 'Slot',
			lblSlotValue: 'Slot Value',
			lblSlotPosition: 'Slot Span',
			lblOriginalValue: 'Real Value',
			lblLeftBtnText: 'Abandon Changes',
			lblRightBtnText: 'Save changes',
			lblBtnMst: 'Abandon changes? Click "Confirm" to save.',
			lblDeleteHint: 'Confirm to delete current utterance?'
		}
	},
	asr: {
		lblReceiveResult: 'Recognition result received:',
		lblRecordStart: 'Recording starts',
		lblRecordEnd: 'End of recording',
		lblNoCapture: 'Nothing was recorded, please try again',
		lblRecognizeFailed: 'Recognition failed, error stack:',
		lblRecordReady: 'Button ready!'
	}
}
