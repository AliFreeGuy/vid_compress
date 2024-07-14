# @app.task(bind=True)
# def process_job(self, job_id):
#     """
#     takes filename as argument and scans it and returns result.
#     """
#     ...
#     # task progres state
#     progress = 0
#     print 'generating input'
#     with file as csvfile:
#         total = sum(1 for row in csvfile)
#         emailreader = csv.reader(csvfile)
#         for email in emailreader:
#             ...

#             # update task progress
#             progress = progress + 1
#             percentage = int((progress * 100) / float(total))
#             self.update_state(state='PROGRESS', meta={'progress': percentage, 'scanned': progress})
#             print 'percentage ', percentage
#             print result

#     # write files
#     ...
#     return result_count_data


# class ProgressView(APIView):
#     """
#     return progress of job id task
#     """

#     def get(self, request, *args, **kwargs):
#         # wait for first time
#         time.sleep(1)
#         # get task id from AsyncResult returned when you call task_name.delay()
#         task_id = request.query_params.get('task_id')
#         task = process_job.AsyncResult(task_id)
#         progress = 0
#         if task.status == 'SUCCESS':
#             progress = 100
#         elif task.status == 'FAILURE':
#             progress = 0
#         elif task.status == 'PROGRESS':
#             progress = task.info.get('progress')  # needs to be set by task

#         return Response({'progress': progress, 'task_status': task.status},
#                         status=status.HTTP_200_OK)