import traceback
from datetime import datetime

import requests
from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource

from ..document_management_app import db, logger
from ..token import token_required
from .database.models import (ADM_FORM_MASTER, ADM_FORM_SUBMISSION,
                              ADM_SETTING_MAPPING, ADM_SYS_SETTING,
                              ADM_USR_AUTH, ADM_USR_MASTER, ADM_WORKFLOW_MASTER)

api = Namespace(path = "/document", name = "Camunda Tasklist")

header_token = api.parser()
header_token.add_argument("access-token", location = "headers")

def get_camunda_rest_api_url():
	camunda_server = (
		db.session.query(
			ADM_SETTING_MAPPING.Additional_Name,
			ADM_SETTING_MAPPING.Additional_Value
		)
		.filter(ADM_SETTING_MAPPING.Sys_ID == ADM_SYS_SETTING.Sys_ID)
		.filter(ADM_SYS_SETTING.Sys_Name == "WORKFLOW SERVER")
		.all()
	)

	if not camunda_server:
		return None
	else:
		camunda_server_ip = None
		camunda_port = None

		for row in camunda_server:
			if row.Additional_Name == "CAMUNDA_SERVER_IP":
				camunda_server_ip = row.Additional_Value

			elif row.Additional_Name == "PORT":
				camunda_port = row.Additional_Value

		if camunda_server_ip and camunda_port:
			return "http://" + camunda_server_ip + ":" + camunda_port
		else:
			return None

# GET, POST
@api.route("/task")
@api.expect(header_token)
class Task(Resource):
	# Get ALL Tasks
	@api.doc(
		description = "Get ALL Tasks",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				result = requests.get(camunda_server + "/engine-rest/task")
				response = result.json()
				return make_response(jsonify(response), result.status_code)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

	# Get ALL Tasks of Single User
	@api.doc(
		description = "Get ALL Tasks of Single User",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self):
		try:
			args = request.get_json()

			if args["User_ID"]:
				user = (
					db.session.query(ADM_USR_AUTH)
					.filter(ADM_USR_AUTH.User_ID == args["User_ID"])
					.first()
				)

				if not user:
					response = {"error": "User not found"}
					return make_response(jsonify(response), 200)
				else:
					camunda_server = get_camunda_rest_api_url()

					if not camunda_server:
						response = {"error": "Kindly contact Administrator"}
						return make_response(jsonify(response), 403)
					else:
						result = requests.post(
							camunda_server + "/engine-rest/task",
							json = { "assignee": user.User_Name }
						)
						response = result.json()
						return make_response(jsonify(response), 200)

			else:
				return None
			
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# GET
@api.route("/task/<Task_ID>")
@api.expect(header_token)
class SingleTask(Resource):
	# Get Single Task
	@api.doc(
		description = "Get Single Task",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Task_ID):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				result = requests.get(camunda_server + "/engine-rest/task/" + Task_ID)
				response = result.json()
				
				if response:
					return make_response(jsonify(response), result.status_code)
				else:
					submission = (
						db.session.query(ADM_FORM_SUBMISSION)
						.filter(ADM_FORM_SUBMISSION.Task_ID == Task_ID)
						.first()
					)

					result = requests.get(camunda_server + "/engine-rest/history/process-instance/" + submission.Process_Instance_ID)

					if result.status_code == 200:
						response = result.json()
						return make_response(jsonify(response), 200)

					else:
						response = {"error": "Process not found"}
						return make_response(jsonify(response), 200)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# GET
@api.route("/task/user/<User_ID>")
@api.expect(header_token)
class UserTasks(Resource):
	# Get Single User's All Tasks
	@api.doc(
		description = "Get Single User's All Tasks",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, User_ID):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				user = (
					db.session.query(ADM_USR_AUTH)
					.filter(ADM_USR_AUTH.User_ID == User_ID)
					.first()
				)

				if not user:
					response = {"error": "User not found"}
					return make_response(jsonify(response), 200)
				else:
					result = requests.get(camunda_server + "/engine-rest/task?assignee=" + user.User_Name)
					response = result.json()
					return make_response(jsonify(response), result.status_code)
			
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# POST
@api.route("/task/<Process_Instance_ID>/claim")
@api.expect(header_token)
class ClaimTask(Resource):
	# Claim Task
	@api.doc(
		description = "Claim Task",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self, Process_Instance_ID):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 200)
			else:
				args = request.get_json()

				if "Approver1" in args:
					temp = requests.post(
						camunda_server + "/engine-rest/task",
						json = { "processInstanceId": Process_Instance_ID }
					)
					task = temp.json()
					task_id = task[0]["id"]
					
					result = requests.post(
						camunda_server + "/engine-rest/task/" + task_id + "/claim",
						json = { "userId": args["Approver1"].replace(".", "") }
					)

					if result.status_code == 204:
						temp = requests.post(
							camunda_server + "/engine-rest/task",
							json = { "processInstanceId": Process_Instance_ID }
						)
						task = temp.json()
						task_id = task[0]["id"]
						task_name = task[0]["name"]

						submission = (
							db.session.query(ADM_FORM_SUBMISSION)
							.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
							.first()
						)

						if submission:
							assignee = (
								db.session.query(ADM_USR_MASTER)
								.filter(ADM_USR_AUTH.User_ID == ADM_USR_MASTER.User_ID)
								.filter(ADM_USR_AUTH.User_Name == args["Approver1"])
								.first()
							)

							submission.Task_ID = task_id
							submission.Status = task_name + (" (" + assignee.Preferred_Name + ")" if assignee else "")
							db.session.commit()

						response = {"success": "Task claimed"}
						return make_response(jsonify(response), 200)
					else:
						response = result.json()
						return make_response(jsonify(response), result.status_code)

				elif "Approver" in args:
					temp = requests.post(
						camunda_server + "/engine-rest/task",
						json = { "processInstanceId": Process_Instance_ID }
					)
					task = temp.json()
					task_id = task[0]["id"]
					
					result = requests.post(
						camunda_server + "/engine-rest/task/" + task_id + "/claim",
						json = { "userId": args["Approver"].replace(".", "") }
					)

					if result.status_code == 204:
						temp = requests.post(
							camunda_server + "/engine-rest/task",
							json = { "processInstanceId": Process_Instance_ID }
						)
						task = temp.json()
						task_id = task[0]["id"]
						task_name = task[0]["name"]

						submission = (
							db.session.query(ADM_FORM_SUBMISSION)
							.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
							.first()
						)

						if submission:
							assignee = (
								db.session.query(ADM_USR_MASTER)
								.filter(ADM_USR_AUTH.User_ID == ADM_USR_MASTER.User_ID)
								.filter(ADM_USR_AUTH.User_Name == args["Approver"])
								.first()
							)

							submission.Task_ID = task_id
							submission.Status = task_name + (" (" + assignee.Preferred_Name + ")" if assignee else "")
							db.session.commit()

						response = {"success": "Task claimed"}
						return make_response(jsonify(response), 200)
					else:
						response = result.json()
						return make_response(jsonify(response), result.status_code)

				else:
					response = {"error": "No Approver selected"}
					return make_response(jsonify(response), 200)
			
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# POST
@api.route("/task/<Process_Instance_ID>/unclaim")
@api.expect(header_token)
class UnclaimTask(Resource):
	# Unclaim Task
	@api.doc(
		description = "Unclaim Task",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self, Process_Instance_ID):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 200)
			else:
				temp = requests.post(
					camunda_server + "/engine-rest/task",
					json = { "processInstanceId": Process_Instance_ID }
				)
				task = temp.json()
				task_id = task[0]["id"]
				
				result = requests.post(
					camunda_server + "/engine-rest/task/" + task_id + "/unclaim"
				)

				if result.status_code == 204:
					response = {"success": "Task unclaimed"}
					return make_response(jsonify(response), 200)

				else:
					response = result.json()
					return make_response(jsonify(response), 200)
			
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# GET
@api.route("/process/<Process_Instance_ID>")
@api.expect(header_token)
class SingleTask(Resource):
	# Get Single Process
	@api.doc(
		description = "Get Single Process",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Process_Instance_ID):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				result = requests.get(camunda_server + "/engine-rest/task?processInstanceId=" + Process_Instance_ID)
				response = result.json()
				
				if response:
					return make_response(jsonify(response), result.status_code)
				else:
					submission = (
						db.session.query(ADM_FORM_SUBMISSION)
						.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
						.first()
					)

					result = requests.get(camunda_server + "/engine-rest/history/process-instance/" + submission.Process_Instance_ID)

					if result.status_code == 200:
						response = result.json()
						return make_response(jsonify(response), 200)

					else:
						response = {"error": "Process not found"}
						return make_response(jsonify(response), 200)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# POST
@api.route("/process/<Process_Instance_ID>/task/<Task_ID>/complete")
@api.expect(header_token)
class SingleTaskVariables(Resource):
	# Complete Task
	@api.doc(
		description = "Complete Task",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self, Process_Instance_ID, Task_ID):
		try:
			args = request.get_json()
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				temp = requests.get(camunda_server + "/engine-rest/task/" + Task_ID)
				task = temp.json()
				task_definition_key = task["taskDefinitionKey"]

				if not task:
					response = {"error": "Unable to get Task"}
					return make_response(jsonify(response), 403)
				else:
					if (
						task_definition_key == "Activity_Submit_Form" or 
						task_definition_key == "Activity_Approve_Expenses" or 
						task_definition_key == "Activity_Approve_Allowance" or 
						task_definition_key == "Activity_Finance_Member_Verify" or 
						task_definition_key == "Activity_HR_Member_Verify" or 
						task_definition_key == "Activity_Get_Customer_Signature" or 
						task_definition_key == "Activity_Review_Sign" or 
						task_definition_key == "Activity_1st_Approval" or 
						task_definition_key == "Activity_2nd_Approval" or 
						task_definition_key == "Activity_System_Check_Amount" or 
						task_definition_key == "Activity_Check_CA_TR" or 
						task_definition_key == "Activity_Admin_Booking" or
						task_definition_key == "Activity_Make_Payment"
					):
						submission = (
							db.session.query(ADM_FORM_MASTER.Form_Name.label("Form_Name"))
							.filter(ADM_FORM_MASTER.ID == ADM_FORM_SUBMISSION.Form_ID)
							.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
							.filter(ADM_FORM_SUBMISSION.Task_ID == Task_ID)
							.first()
						)

						if not submission:
							response = {"error": "Form Submission not found"}
							return make_response(jsonify(response), 200)
						else:
							if task_definition_key == "Activity_Submit_Form":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"action": { "value": args["action"] }
										},
										"withVariablesInReturn": True
									}
								)

							if (
								"OUTSTATION" in submission.Form_Name.upper() and 
								(task_definition_key == "Activity_Check_CA_TR" or 
								task_definition_key == "Activity_Admin_Booking" or 
								task_definition_key == "Activity_Make_Payment")
							):
								if task_definition_key == "Activity_Check_CA_TR":
									if "travelrequest" in args and "cashadvance" in args:
										complete_result = requests.post(
											camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
											headers = { "Content-Type": "application/json" },
											json = {
												"variables": {
													"travelrequest": { "value": args["travelrequest"] },
													"cashadvance": { "value": args["cashadvance"] }
												},
												"withVariablesInReturn": True
											}
										)

									elif "travelrequest" in args and "cashadvance" not in args:
										complete_result = requests.post(
											camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
											headers = { "Content-Type": "application/json" },
											json = {
												"variables": {
													"travelrequest": { "value": args["travelrequest"] }
												},
												"withVariablesInReturn": True
											}
										)

									elif "travelrequest" not in args and "cashadvance" in args:
										complete_result = requests.post(
											camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
											headers = { "Content-Type": "application/json" },
											json = {
												"variables": {
													"cashadvance": { "value": args["cashadvance"] }
												},
												"withVariablesInReturn": True
											}
										)

								elif task_definition_key == "Activity_Admin_Booking" or task_definition_key == "Activity_Make_Payment":
									complete_result = requests.post(
										camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
										headers = { "Content-Type": "application/json" }
									)

									if complete_result.status_code == 200 or complete_result.status_code == 204:
										submission_count = (
											db.session.query(ADM_FORM_SUBMISSION)
											.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
											.count()
										)

										if submission_count > 1:
											submission = (
												db.session.query(ADM_FORM_SUBMISSION)
												.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
												.filter(ADM_FORM_SUBMISSION.Task_ID == Task_ID)
												.first()
											)

											if submission:
												db.session.delete(submission)
												db.session.commit()

										else:
											temp = requests.post(
												camunda_server + "/engine-rest/task",
												json = { "processInstanceId": Process_Instance_ID }
											)
											task = temp.json()
											
											if not task or len(task) == 0:
												history = requests.get(
													camunda_server + "/engine-rest/history/process-instance/" + Process_Instance_ID
												)

												if history.status_code == 200:
													response = history.json()

													if response["state"] == "COMPLETED":
														submission = (
															db.session.query(ADM_FORM_SUBMISSION)
															.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
															.first()
														)

														if submission:
															submission.Status = "COMPLETED"
															submission.Task_ID = None
															db.session.commit()

												return make_response(jsonify({"success": "Process Completed"}), 200)

											else:
												next_task_id = []
												task_definition_key = []
												index = 0

												for row in task:
													task_id = row["id"]
													next_task_id.append(task_id)
													task_definition_key.append(row["taskDefinitionKey"])
													task_name = row["name"]
													task_assignee = row["assignee"]

													submission = (
														db.session.query(ADM_FORM_SUBMISSION)
														.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
														.first()
													)

													if submission and index == 0:
														assignee = (
															db.session.query(ADM_USR_MASTER)
															.filter(ADM_USR_AUTH.User_ID == ADM_USR_MASTER.User_ID)
															.filter(ADM_USR_AUTH.User_Name == task_assignee)
															.first()
														)

														submission.Task_ID = task_id
														submission.Status = task_name + (" (" + assignee.Preferred_Name + ")" if assignee else "")
														db.session.commit()

													elif submission and index > 0:
														new_task = ADM_FORM_SUBMISSION(
															Process_Instance_ID = submission.Process_Instance_ID,
															Task_ID = task_id,
															Submission_ID = submission.Submission_ID,
															Form_ID = submission.Form_ID,
															Org_ID = submission.Org_ID,
															BU_ID = submission.BU_ID,
															Dept_ID = submission.Dept_ID,
															Project_Code = submission.Project_Code,
															Total = submission.Total,
															Creator = submission.Creator,
															Date_Created = submission.Date_Created,
															Status = task_name + (" (" + assignee.Preferred_Name + ")" if assignee else ""),
															Comments = "",
															Approver1 = submission.Approver1,
															Approver2 = submission.Approver2,
															Data = submission.Data,
														)

														db.session.add(new_task)
														db.session.commit()

													index = index + 1

												response = {
													"success": "Task completed",
													"next_task": ",".join(task_definition_key),
													"next_task_id": ",".join(next_task_id)
												}
												return make_response(jsonify(response), 200)

							elif task_definition_key == "Activity_Approve_Expenses" or task_definition_key == "Activity_Approve_Allowance":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"approved": { "value": args["approved"] }
										},
										"withVariablesInReturn": True
									}
								)

							elif task_definition_key == "Activity_Finance_Member_Verify" or task_definition_key == "Activity_HR_Member_Verify":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"verified": { "value": args["verified"] }
										},
										"withVariablesInReturn": True
									}
								)

							elif task_definition_key == "Activity_Get_Customer_Signature":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"signed": { "value": args["signed"] }
										},
										"withVariablesInReturn": True
									}
								)

							elif task_definition_key == "Activity_Review_Sign":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"continue": { "value": args["continue"] }
										},
										"withVariablesInReturn": True
									}
								)

							elif task_definition_key == "Activity_1st_Approval":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"firstapproved": { "value": args["firstapproved"] }
										},
										"withVariablesInReturn": True
									}
								)

							elif task_definition_key == "Activity_2nd_Approval":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"secondapproved": { "value": args["secondapproved"] }
										},
										"withVariablesInReturn": True
									}
								)

							elif task_definition_key == "Activity_System_Check_Amount":
								complete_result = requests.post(
									camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
									headers = { "Content-Type": "application/json" },
									json = {
										"variables": {
											"exceed2k": { "value": args["exceed2k"] }
										},
										"withVariablesInReturn": True
									}
								)

					else:
						complete_result = requests.post(
							camunda_server + "/engine-rest/task/" + Task_ID + "/complete",
							headers = { "Content-Type": "application/json" }
						)
					
					if complete_result.status_code == 200 or complete_result.status_code == 204:
						temp = requests.post(
							camunda_server + "/engine-rest/task",
							json = { "processInstanceId": Process_Instance_ID }
						)
						task = temp.json()
						
						if not task or len(task) == 0:
							history = requests.post(
								camunda_server + "/engine-rest/history/process-instance/" + Process_Instance_ID
							)

							if history.status_code == 200:
								response = history.json()

								if response["state"] == "COMPLETED":
									submission = (
										db.session.query(ADM_FORM_SUBMISSION)
										.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
										.first()
									)

									if submission:
										if task_definition_key == "Activity_Submit_Form" and args["action"] == "CANCEL":
											submission.Status = "CANCELLED"
										else:
											submission.Status = "COMPLETED"
											
										submission.Task_ID = None
										db.session.commit()

							return make_response(jsonify({"success": "Process Completed"}), 200)

						else:
							next_task_id = []
							task_definition_key = []
							index = 0

							for row in task:
								task_id = row["id"]
								next_task_id.append(task_id)
								task_definition_key.append(row["taskDefinitionKey"])
								task_name = row["name"]
								task_assignee = row["assignee"]

								submission = (
									db.session.query(ADM_FORM_SUBMISSION)
									.filter(ADM_FORM_SUBMISSION.Process_Instance_ID == Process_Instance_ID)
									.first()
								)

								if submission and index == 0:
									assignee = (
										db.session.query(ADM_USR_MASTER)
										.filter(ADM_USR_AUTH.User_ID == ADM_USR_MASTER.User_ID)
										.filter(ADM_USR_AUTH.User_Name == task_assignee)
										.first()
									)

									submission.Task_ID = task_id
									submission.Status = task_name + (" (" + assignee.Preferred_Name + ")" if assignee else "")
									db.session.commit()

								elif submission and index > 0:
									new_task = ADM_FORM_SUBMISSION(
										Process_Instance_ID = submission.Process_Instance_ID,
										Task_ID = task_id,
										Submission_ID = submission.Submission_ID,
										Form_ID = submission.Form_ID,
										Org_ID = submission.Org_ID,
										BU_ID = submission.BU_ID,
										Dept_ID = submission.Dept_ID,
										Project_Code = submission.Project_Code,
										Total = submission.Total,
										Creator = submission.Creator,
										Date_Created = submission.Date_Created,
										Status = task_name + (" (" + assignee.Preferred_Name + ")" if assignee else ""),
										Comments = "",
										Approver1 = submission.Approver1,
										Approver2 = submission.Approver2,
										Data = submission.Data,
									)

									db.session.add(new_task)
									db.session.commit()

								index = index + 1

							response = {
								"success": "Task completed",
								"next_task": ",".join(task_definition_key),
								"next_task_id": ",".join(next_task_id)
							}
							return make_response(jsonify(response), 200)

					elif complete_result.status_code == 400:
						response = {"error": complete_result.json()["message"] if "message" in complete_result.json() else "Variable value or type is invalid"}
						return make_response(jsonify(response), complete_result.status_code)

					elif complete_result.status_code == 500:
						response = {"error": complete_result.json()["message"] if "message" in complete_result.json() else "Task does not exist or the corresponding process instance could not be resumed successfully"}
						return make_response(jsonify(response), complete_result.status_code)

					else:
						response = complete_result.json()
						return make_response(jsonify(response), complete_result.status_code)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# POST
@api.route("/process-definition/<Deployment_ID>/start")
@api.expect(header_token)
class StartProcess(Resource):
	# Start a New Process
	@api.doc(
		description = "Start a New Process",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def post(self, Deployment_ID):
		try:
			args = request.get_json()
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				result = requests.post(
					camunda_server + "/engine-rest/process-definition/" + Deployment_ID + "/start",
					json = { "businessKey": args["businessKey"] }
				)
				result_json = result.json()
				process_instance_id = result_json["id"]

				temp = requests.post(
					camunda_server + "/engine-rest/task",
					json = { "processInstanceId": process_instance_id }
				)
				task = temp.json()
				task_id = task[0]["id"]
				task_name = task[0]["name"]
				task_assignee = task[0]["assignee"]

				form = (
					db.session.query(ADM_FORM_MASTER)
					.filter(ADM_FORM_MASTER.Workflow_ID == ADM_WORKFLOW_MASTER.ID)
					.filter(ADM_WORKFLOW_MASTER.Deployment_ID == Deployment_ID)
					.first()
				)

				assignee = (
					db.session.query(ADM_USR_MASTER)
					.filter(ADM_USR_AUTH.User_ID == ADM_USR_MASTER.User_ID)
					.filter(ADM_USR_AUTH.User_Name == task_assignee)
					.first()
				)

				new_form_submission = ADM_FORM_SUBMISSION(
					Process_Instance_ID = process_instance_id,
					Task_ID = task_id,
					Submission_ID = "",
					Form_ID = form.ID if form else None,
					Org_ID = request.headers["Org_ID"] if "Org_ID" in request.headers else None,
					BU_ID = request.headers["BU_ID"] if "BU_ID" in request.headers else None,
					Dept_ID = request.headers["Dept_ID"] if "Dept_ID" in request.headers else None,
					Creator = request.headers["Claimant"] if "Claimant" in request.headers else None,
					Project_Code = request.headers["Project_Code"] if "Project_Code" in request.headers else None,
					Total = request.headers["Total"] if "Total" in request.headers else None,
					Data = args["variables"],
					Date_Created = datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
					Status = task_name + (" (" + assignee.Preferred_Name + ")" if assignee else "")
				)

				db.session.add(new_form_submission)
				db.session.commit()

				if "Claimant" in request.headers:
					user = (
						db.session.query(ADM_USR_AUTH)
						.filter(ADM_USR_AUTH.User_ID == request.headers["Claimant"])
						.first()
					)

					if user:
						claim = requests.post(
							camunda_server + "/engine-rest/task/" + task_id + "/claim",
							json = { "userId": user.User_Name }
						)

				response = {
					"success": "Process started successfully",
					"Process_Instance_ID": process_instance_id,
					"Task_ID": task_id
				}

				return make_response(jsonify(response), result.status_code)
			
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)
		
		finally:
			db.session.close()

# GET
@api.route("/process-definition/<Process_Definition_ID>")
@api.expect(header_token)
class ProcessDefinition(Resource):
	# Get Single Process Definition
	@api.doc(
		description = "Get Single Process Definition",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Process_Definition_ID):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				result = requests.get(camunda_server + "/engine-rest/process-definition/" + Process_Definition_ID)
				response = result.json()
				return make_response(jsonify(response), result.status_code)
			
		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# GET
@api.route("/process-definition/<Process_Definition_ID>/xml")
@api.expect(header_token)
class ProcessDefinitionXML(Resource):
	# Get Process Definition XML
	@api.doc(
		description = "Get Process Definition XML",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self, Process_Definition_ID):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				result = requests.get(camunda_server + "/engine-rest/process-definition/" + Process_Definition_ID + "/xml")
				response = result.json()
				return make_response(jsonify(response), result.status_code)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())
			
			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)

		finally:
			db.session.close()

# GET
@api.route("/process-instance")
@api.expect(header_token)
class Process(Resource):
	# Get ALL Process Instances
	@api.doc(
		description = "Get ALL Process Instances",
		responses = {
			200: "OK",
			403: "Error"
		}
	)
	@token_required
	def get(self):
		try:
			camunda_server = get_camunda_rest_api_url()

			if not camunda_server:
				response = {"error": "Kindly contact Administrator"}
				return make_response(jsonify(response), 403)
			else:
				result = requests.get(camunda_server + "/engine-rest/process-instance")
				response = result.json()
				return make_response(jsonify(response), result.status_code)

		except Exception as e:
			logger.error(str(type(e)))
			logger.error(str(e))
			logger.error(traceback.format_exc())

			response = {
				"traceback": traceback.format_exc(),
				"exception": str(type(e)),
				"error": str(e)
			}
			return make_response(jsonify(response), 403)
		
		finally:
			db.session.close()
