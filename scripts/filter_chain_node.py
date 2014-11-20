#!/usr/bin/env python

import roslib; roslib.load_manifest('ros_vision')
import rospy
from RosVision.filter_chain import FilterChain
from RosVision.Filters.filter_factory import FilterFactory
import ros_vision.srv
import ros_vision.msg
from RosVision.io_manager import IOManager

def update_filter_topic():
    msg = ros_vision.msg.FilterList()
    for f in fc.get_filters():
        msg.filters.append(create_filter_message(f))

    filter_topic.publish(msg)

def create_filter_message(f):
        descriptor = f.get_descriptor()

        filter = ros_vision.msg.Filter()
        filter.name = f.name
        filter.description = descriptor.description

        for i in descriptor.get_inputs():
            d = ros_vision.msg.IODescriptor()
            name = i.get_name()
            d.name = name
            d.type = str(i.get_io_type().get_ros_type()._type)
            d.topic = IOManager().format_topic_name(f.get_io_name(name))
            filter.inputs.append(d)

        for o in descriptor.get_outputs():
            d = ros_vision.msg.IODescriptor()
            name = o.get_name()
            d.name = name
            d.type = str(o.get_io_type().get_ros_type()._type)
            d.topic = IOManager().format_topic_name(f.get_io_name(name))
            filter.outputs.append(d)

        for p in descriptor.get_parameters():
            parameter = ros_vision.msg.Parameter()
            parameter.name = p.get_name()
            parameter.description = p.get_description()
            parameter.type = p.get_type().__name__
            parameter.default = str(p.get_default_value())
            parameter.min = str(p.get_min_value())
            parameter.max = str(p.get_max_value())
            filter.parameters.append(parameter)

        return filter

def create_filter(req):
    params = {}
    prefix = "%s/%s/" % (rospy.get_name(), req.name)
    for p in rospy.get_param_names():
        if p.startswith(prefix):
            params[p[len(prefix):]] = rospy.get_param(p)

    fc.create_filter(req.name, req.type, params)
    update_filter_topic()

    return ros_vision.srv.CreateFilterResponse()

def get_filter_info(req):
    return create_filter_message(FilterFactory.create_filter("", req.type))

def list_filters(req):
    res = ros_vision.srv.ListFiltersResponse();
    res.filters = FilterFactory.list_filters()

    return res

rospy.init_node('filter_chain_node')

fc = FilterChain()

create_filter_service = rospy.Service('~create_filter', ros_vision.srv.CreateFilter, create_filter)
get_filter_info_service = rospy.Service('~get_filter_info', ros_vision.srv.GetFilterInfo, get_filter_info)
list_filters_service = rospy.Service('~list_filters', ros_vision.srv.ListFilters, list_filters)
filter_topic = rospy.Publisher('~filters', ros_vision.msg.FilterList, queue_size=1, latch=True)
rate = rospy.Rate(20)

while not rospy.is_shutdown():
    fc.execute()
    rate.sleep()

