import boto3
from django.shortcuts import render
import time
import datetime

# client_resource = boto3.resource('cloudwatch')
client = boto3.client('cloudwatch')
client_log = boto3.client('logs')


# Create your views here.

def hello(request):
    # now = datetime.now()
    # datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S.%fZ')
    # t = int((datetime.datetime.now() - datetime.timedelta(hours=1)).timestamp())
    # print(t)
    # d = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
    # print(d)
    now = datetime.datetime.now()
    start_datetime = int(now.timestamp())
    end_datetime = int((now - datetime.timedelta(minutes=5)).timestamp())

    response = client_log.start_query(
        logGroupName="/aws/lambda/OrivetApi-OrivetNestedSta-AnimalGetByIdFunction045-GQhyRG6XvWeP",
        queryString=
        # "\
        #     fields @timestamp, @message \
        #     | sort @timestamp desc \
        #     | limit 10 \
        #     ",
        "fields @timestamp \
            | filter level = 'ERROR' \
            | sort @timestamp desc \
            | limit 5  \
            | display @message",
        # endTime=1713711470217,
        # startTime=1713700522091,
        startTime=end_datetime,
        endTime=start_datetime
        # limit=5
    )
    query_id = response['queryId']

    results = None
    while results == None or results['status'] == 'Running':
        time.sleep(1)
        results = client_log.get_query_results(
            queryId=query_id
        )
    timestamp_s = 1713700522091 / 1000.0  # Convert milliseconds to seconds
    datetime_obj = datetime.datetime.fromtimestamp(timestamp_s)
    print(datetime_obj)
    now = datetime.datetime.now()
    five_min_back = now - datetime.timedelta(minutes=5)
    print(now)
    print(five_min_back)


    for result in results['results']:
        print(result[0].get('value'))
        print('======')
    # response = client_log.filter_log_events(
    #     logGroupName='/aws/lambda/OrivetApi-OrivetNestedSta-AnimalGetByIdFunction045-GQhyRG6XvWeP',
    #     # filterPattern="fields @timestamp \
    #     #     | filter level = 'ERROR' \
    #     #     | sort @timestamp desc \
    #     #     | limit 5 \
    #     #     | display @message"
    #     limit= 20,
    #         startTime=1711365890625,
    #         endTime=1711365890695
    #     )
    # print(response)
    
    return render(request, 'hello.html', {'resource': []})
    

def hello1(request):
    # Define alarm parameters
    alarm_name = 'lambda-errors-alarm'
    alarm_description = 'Alarm for Lambda function errors'
    metric_name = 'Errors'
    namespace = 'AWS/Lambda'
    statistic = 'SampleCount'
    comparison_operator = 'GreaterThanOrEqualToThreshold'
    threshold = 3.0
    period = 10
    evaluation_periods = 1
    actions_enabled = True
    alarm_actions = [
        'arn:aws:sns:ap-southeast-2:058188477434:LambdaErrorMetrix']
    dimensions = [
        {
            'Name': 'Resource',
            'Value': 'arn:aws:lambda:ap-southeast-2:058188477434:function:OrivetApi-OrivetNestedSta-AnimalGetByIdFunction045-GQhyRG6XvWeP'
        }
    ]
    metrics = [
        {
            'Id': 'animalGetbyidmetrix',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'OrivetAPI',
                    'MetricName': 'Errors',
                    'Dimensions': [
                        {
                            'Name': 'Resource',
                            'Value': 'arn:aws:lambda:ap-southeast-2:058188477434:function:OrivetApi-OrivetNestedSta-AnimalGetByIdFunction045-GQhyRG6XvWeP'
                        },
                    ]
                },
                'Period': 60,
                'Stat': 'Sum',
                'Unit':  'Count' 
            },
           
        },
    ]

    resource = client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=alarm_description,
        # MetricName=metric_name,
        # Namespace=namespace,
        # Statistic=statistic,
        ComparisonOperator=comparison_operator,
        Threshold=threshold,
        # Period=period,
        EvaluationPeriods=evaluation_periods,
        AlarmActions=alarm_actions,
        # Dimensions=dimensions,
        ActionsEnabled=actions_enabled,
        Metrics=metrics
    )
    time_str = '2024-04-21T12:18:27.912Z'
    time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    start_time = int(time_obj.timestamp() * 1000)

    # start_time = int(time.mktime(time.strptime("2024-04-21T12:18:27.912Z", "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())) 
    print(start_time)

    return render(request, 'hello.html', {'resource': start_time})
