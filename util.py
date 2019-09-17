# import connection
#
#
# @connection.connection_handler
# def change_view_number(cursor, question_data):
#     cursor.execute('''
#                     UPDATE question SET view_number=+1 WHERE title= %(title)s;'''
#                    , question_data)
#     question = cursor.fetchall()
#     return question
