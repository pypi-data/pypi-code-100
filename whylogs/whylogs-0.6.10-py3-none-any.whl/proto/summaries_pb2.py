# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: summaries.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import messages_pb2 as messages__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fsummaries.proto\x1a\x0emessages.proto\x1a\x19google/protobuf/any.proto\x1a\x1cgoogle/protobuf/struct.proto\"D\n\x12UniqueCountSummary\x12\x10\n\x08\x65stimate\x18\x01 \x01(\x01\x12\r\n\x05upper\x18\x02 \x01(\x01\x12\r\n\x05lower\x18\x03 \x01(\x01\"~\n\x16\x46requentStringsSummary\x12\x33\n\x05items\x18\x01 \x03(\x0b\x32$.FrequentStringsSummary.FrequentItem\x1a/\n\x0c\x46requentItem\x12\r\n\x05value\x18\x01 \x01(\t\x12\x10\n\x08\x65stimate\x18\x02 \x01(\x01\"\x96\x02\n\x16\x46requentNumbersSummary\x12;\n\x07\x64oubles\x18\x01 \x03(\x0b\x32*.FrequentNumbersSummary.FrequentDoubleItem\x12\x37\n\x05longs\x18\x02 \x03(\x0b\x32(.FrequentNumbersSummary.FrequentLongItem\x1a\x43\n\x12\x46requentDoubleItem\x12\x10\n\x08\x65stimate\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\x01\x12\x0c\n\x04rank\x18\x03 \x01(\x05\x1a\x41\n\x10\x46requentLongItem\x12\x10\n\x08\x65stimate\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\x03\x12\x0c\n\x04rank\x18\x03 \x01(\x05\"\x7f\n\x14\x46requentItemsSummary\x12\x31\n\x05items\x18\x01 \x03(\x0b\x32\".FrequentItemsSummary.FrequentItem\x1a\x34\n\x0c\x46requentItem\x12\x10\n\x08\x65stimate\x18\x01 \x01(\x03\x12\x12\n\njson_value\x18\x02 \x01(\t\"\xa2\x01\n\x0e\x43harPosSummary\x12\x16\n\x0e\x63haracter_list\x18\x01 \x01(\t\x12\x35\n\x0c\x63har_pos_map\x18\x02 \x03(\x0b\x32\x1f.CharPosSummary.CharPosMapEntry\x1a\x41\n\x0f\x43harPosMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1d\n\x05value\x18\x02 \x01(\x0b\x32\x0e.NumberSummary:\x02\x38\x01\"\xd7\x01\n\x0eStringsSummary\x12)\n\x0cunique_count\x18\x01 \x01(\x0b\x32\x13.UniqueCountSummary\x12)\n\x08\x66requent\x18\x02 \x01(\x0b\x32\x17.FrequentStringsSummary\x12\x1e\n\x06length\x18\x03 \x01(\x0b\x32\x0e.NumberSummary\x12$\n\x0ctoken_length\x18\x04 \x01(\x0b\x32\x0e.NumberSummary\x12)\n\x10\x63har_pos_tracker\x18\x05 \x01(\x0b\x32\x0f.CharPosSummary\"\x9d\x01\n\rSchemaSummary\x12$\n\rinferred_type\x18\x01 \x01(\x0b\x32\r.InferredType\x12\x33\n\x0btype_counts\x18\x02 \x03(\x0b\x32\x1e.SchemaSummary.TypeCountsEntry\x1a\x31\n\x0fTypeCountsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03:\x02\x38\x01\"\x80\x01\n\x10HistogramSummary\x12\r\n\x05start\x18\x01 \x01(\x01\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x01\x12\r\n\x05width\x18\x03 \x01(\x01\x12\x0e\n\x06\x63ounts\x18\x04 \x03(\x03\x12\x0b\n\x03max\x18\x05 \x01(\x01\x12\x0b\n\x03min\x18\x06 \x01(\x01\x12\x0c\n\x04\x62ins\x18\x07 \x03(\x01\x12\t\n\x01n\x18\x08 \x01(\x03\"=\n\x0fQuantileSummary\x12\x11\n\tquantiles\x18\x01 \x03(\x01\x12\x17\n\x0fquantile_values\x18\x02 \x03(\x01\"\x94\x02\n\rNumberSummary\x12\r\n\x05\x63ount\x18\x01 \x01(\x04\x12\x0b\n\x03min\x18\x02 \x01(\x01\x12\x0b\n\x03max\x18\x03 \x01(\x01\x12\x0c\n\x04mean\x18\x04 \x01(\x01\x12\x0e\n\x06stddev\x18\x05 \x01(\x01\x12$\n\thistogram\x18\x06 \x01(\x0b\x32\x11.HistogramSummary\x12)\n\x0cunique_count\x18\x07 \x01(\x0b\x32\x13.UniqueCountSummary\x12#\n\tquantiles\x18\x08 \x01(\x0b\x32\x10.QuantileSummary\x12\x31\n\x10\x66requent_numbers\x18\t \x01(\x0b\x32\x17.FrequentNumbersSummary\x12\x13\n\x0bis_discrete\x18\n \x01(\x08\"\xf7\x01\n\rColumnSummary\x12\x1b\n\x08\x63ounters\x18\x01 \x01(\x0b\x32\t.Counters\x12\x1e\n\x06schema\x18\x02 \x01(\x0b\x32\x0e.SchemaSummary\x12&\n\x0enumber_summary\x18\x03 \x01(\x0b\x32\x0e.NumberSummary\x12\'\n\x0estring_summary\x18\x04 \x01(\x0b\x32\x0f.StringsSummary\x12-\n\x0e\x66requent_items\x18\x05 \x01(\x0b\x32\x15.FrequentItemsSummary\x12)\n\x0cunique_count\x18\x06 \x01(\x0b\x32\x13.UniqueCountSummary\"\xc5\x01\n\x0e\x44\x61tasetSummary\x12&\n\nproperties\x18\x01 \x01(\x0b\x32\x12.DatasetProperties\x12-\n\x07\x63olumns\x18\x02 \x03(\x0b\x32\x1c.DatasetSummary.ColumnsEntry\x12\x1c\n\x05model\x18\x03 \x01(\x0b\x32\r.ModelSummary\x1a>\n\x0c\x43olumnsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1d\n\x05value\x18\x02 \x01(\x0b\x32\x0e.ColumnSummary:\x02\x38\x01\"0\n\x0cModelSummary\x12 \n\x07metrics\x18\x01 \x01(\x0b\x32\x0f.MetricsSummary\"\x9f\x01\n\x0eMetricsSummary\x12\x1e\n\nmodel_type\x18\x01 \x01(\x0e\x32\n.ModelType\x12\x1e\n\x0broc_fpr_tpr\x18\x02 \x01(\x0b\x32\t.ROCCurve\x12!\n\x0brecall_prec\x18\x03 \x01(\x0b\x32\x0c.RecallCurve\x12*\n\x10\x63onfusion_matrix\x18\x04 \x01(\x0b\x32\x10.ConfusionMatrix\"\x93\x01\n\x0f\x43onfusionMatrix\x12\x0e\n\x06labels\x18\x01 \x03(\t\x12\x14\n\x0ctarget_field\x18\x02 \x01(\t\x12\x19\n\x11predictions_field\x18\x03 \x01(\t\x12\x13\n\x0bscore_field\x18\x04 \x01(\t\x12*\n\x06\x63ounts\x18\x05 \x03(\x0b\x32\x1a.google.protobuf.ListValue\"6\n\x08ROCCurve\x12*\n\x06values\x18\x01 \x03(\x0b\x32\x1a.google.protobuf.ListValue\"9\n\x0bRecallCurve\x12*\n\x06values\x18\x01 \x03(\x0b\x32\x1a.google.protobuf.ListValue\"\x87\x01\n\x10\x44\x61tasetSummaries\x12\x31\n\x08profiles\x18\x01 \x03(\x0b\x32\x1f.DatasetSummaries.ProfilesEntry\x1a@\n\rProfilesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1e\n\x05value\x18\x02 \x01(\x0b\x32\x0f.DatasetSummary:\x02\x38\x01\x42\'\n\x18\x63om.whylogs.core.messageB\tSummariesP\x01\x62\x06proto3')



_UNIQUECOUNTSUMMARY = DESCRIPTOR.message_types_by_name['UniqueCountSummary']
_FREQUENTSTRINGSSUMMARY = DESCRIPTOR.message_types_by_name['FrequentStringsSummary']
_FREQUENTSTRINGSSUMMARY_FREQUENTITEM = _FREQUENTSTRINGSSUMMARY.nested_types_by_name['FrequentItem']
_FREQUENTNUMBERSSUMMARY = DESCRIPTOR.message_types_by_name['FrequentNumbersSummary']
_FREQUENTNUMBERSSUMMARY_FREQUENTDOUBLEITEM = _FREQUENTNUMBERSSUMMARY.nested_types_by_name['FrequentDoubleItem']
_FREQUENTNUMBERSSUMMARY_FREQUENTLONGITEM = _FREQUENTNUMBERSSUMMARY.nested_types_by_name['FrequentLongItem']
_FREQUENTITEMSSUMMARY = DESCRIPTOR.message_types_by_name['FrequentItemsSummary']
_FREQUENTITEMSSUMMARY_FREQUENTITEM = _FREQUENTITEMSSUMMARY.nested_types_by_name['FrequentItem']
_CHARPOSSUMMARY = DESCRIPTOR.message_types_by_name['CharPosSummary']
_CHARPOSSUMMARY_CHARPOSMAPENTRY = _CHARPOSSUMMARY.nested_types_by_name['CharPosMapEntry']
_STRINGSSUMMARY = DESCRIPTOR.message_types_by_name['StringsSummary']
_SCHEMASUMMARY = DESCRIPTOR.message_types_by_name['SchemaSummary']
_SCHEMASUMMARY_TYPECOUNTSENTRY = _SCHEMASUMMARY.nested_types_by_name['TypeCountsEntry']
_HISTOGRAMSUMMARY = DESCRIPTOR.message_types_by_name['HistogramSummary']
_QUANTILESUMMARY = DESCRIPTOR.message_types_by_name['QuantileSummary']
_NUMBERSUMMARY = DESCRIPTOR.message_types_by_name['NumberSummary']
_COLUMNSUMMARY = DESCRIPTOR.message_types_by_name['ColumnSummary']
_DATASETSUMMARY = DESCRIPTOR.message_types_by_name['DatasetSummary']
_DATASETSUMMARY_COLUMNSENTRY = _DATASETSUMMARY.nested_types_by_name['ColumnsEntry']
_MODELSUMMARY = DESCRIPTOR.message_types_by_name['ModelSummary']
_METRICSSUMMARY = DESCRIPTOR.message_types_by_name['MetricsSummary']
_CONFUSIONMATRIX = DESCRIPTOR.message_types_by_name['ConfusionMatrix']
_ROCCURVE = DESCRIPTOR.message_types_by_name['ROCCurve']
_RECALLCURVE = DESCRIPTOR.message_types_by_name['RecallCurve']
_DATASETSUMMARIES = DESCRIPTOR.message_types_by_name['DatasetSummaries']
_DATASETSUMMARIES_PROFILESENTRY = _DATASETSUMMARIES.nested_types_by_name['ProfilesEntry']
UniqueCountSummary = _reflection.GeneratedProtocolMessageType('UniqueCountSummary', (_message.Message,), {
  'DESCRIPTOR' : _UNIQUECOUNTSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:UniqueCountSummary)
  })
_sym_db.RegisterMessage(UniqueCountSummary)

FrequentStringsSummary = _reflection.GeneratedProtocolMessageType('FrequentStringsSummary', (_message.Message,), {

  'FrequentItem' : _reflection.GeneratedProtocolMessageType('FrequentItem', (_message.Message,), {
    'DESCRIPTOR' : _FREQUENTSTRINGSSUMMARY_FREQUENTITEM,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:FrequentStringsSummary.FrequentItem)
    })
  ,
  'DESCRIPTOR' : _FREQUENTSTRINGSSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:FrequentStringsSummary)
  })
_sym_db.RegisterMessage(FrequentStringsSummary)
_sym_db.RegisterMessage(FrequentStringsSummary.FrequentItem)

FrequentNumbersSummary = _reflection.GeneratedProtocolMessageType('FrequentNumbersSummary', (_message.Message,), {

  'FrequentDoubleItem' : _reflection.GeneratedProtocolMessageType('FrequentDoubleItem', (_message.Message,), {
    'DESCRIPTOR' : _FREQUENTNUMBERSSUMMARY_FREQUENTDOUBLEITEM,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:FrequentNumbersSummary.FrequentDoubleItem)
    })
  ,

  'FrequentLongItem' : _reflection.GeneratedProtocolMessageType('FrequentLongItem', (_message.Message,), {
    'DESCRIPTOR' : _FREQUENTNUMBERSSUMMARY_FREQUENTLONGITEM,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:FrequentNumbersSummary.FrequentLongItem)
    })
  ,
  'DESCRIPTOR' : _FREQUENTNUMBERSSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:FrequentNumbersSummary)
  })
_sym_db.RegisterMessage(FrequentNumbersSummary)
_sym_db.RegisterMessage(FrequentNumbersSummary.FrequentDoubleItem)
_sym_db.RegisterMessage(FrequentNumbersSummary.FrequentLongItem)

FrequentItemsSummary = _reflection.GeneratedProtocolMessageType('FrequentItemsSummary', (_message.Message,), {

  'FrequentItem' : _reflection.GeneratedProtocolMessageType('FrequentItem', (_message.Message,), {
    'DESCRIPTOR' : _FREQUENTITEMSSUMMARY_FREQUENTITEM,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:FrequentItemsSummary.FrequentItem)
    })
  ,
  'DESCRIPTOR' : _FREQUENTITEMSSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:FrequentItemsSummary)
  })
_sym_db.RegisterMessage(FrequentItemsSummary)
_sym_db.RegisterMessage(FrequentItemsSummary.FrequentItem)

CharPosSummary = _reflection.GeneratedProtocolMessageType('CharPosSummary', (_message.Message,), {

  'CharPosMapEntry' : _reflection.GeneratedProtocolMessageType('CharPosMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _CHARPOSSUMMARY_CHARPOSMAPENTRY,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:CharPosSummary.CharPosMapEntry)
    })
  ,
  'DESCRIPTOR' : _CHARPOSSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:CharPosSummary)
  })
_sym_db.RegisterMessage(CharPosSummary)
_sym_db.RegisterMessage(CharPosSummary.CharPosMapEntry)

StringsSummary = _reflection.GeneratedProtocolMessageType('StringsSummary', (_message.Message,), {
  'DESCRIPTOR' : _STRINGSSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:StringsSummary)
  })
_sym_db.RegisterMessage(StringsSummary)

SchemaSummary = _reflection.GeneratedProtocolMessageType('SchemaSummary', (_message.Message,), {

  'TypeCountsEntry' : _reflection.GeneratedProtocolMessageType('TypeCountsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SCHEMASUMMARY_TYPECOUNTSENTRY,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:SchemaSummary.TypeCountsEntry)
    })
  ,
  'DESCRIPTOR' : _SCHEMASUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:SchemaSummary)
  })
_sym_db.RegisterMessage(SchemaSummary)
_sym_db.RegisterMessage(SchemaSummary.TypeCountsEntry)

HistogramSummary = _reflection.GeneratedProtocolMessageType('HistogramSummary', (_message.Message,), {
  'DESCRIPTOR' : _HISTOGRAMSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:HistogramSummary)
  })
_sym_db.RegisterMessage(HistogramSummary)

QuantileSummary = _reflection.GeneratedProtocolMessageType('QuantileSummary', (_message.Message,), {
  'DESCRIPTOR' : _QUANTILESUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:QuantileSummary)
  })
_sym_db.RegisterMessage(QuantileSummary)

NumberSummary = _reflection.GeneratedProtocolMessageType('NumberSummary', (_message.Message,), {
  'DESCRIPTOR' : _NUMBERSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:NumberSummary)
  })
_sym_db.RegisterMessage(NumberSummary)

ColumnSummary = _reflection.GeneratedProtocolMessageType('ColumnSummary', (_message.Message,), {
  'DESCRIPTOR' : _COLUMNSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:ColumnSummary)
  })
_sym_db.RegisterMessage(ColumnSummary)

DatasetSummary = _reflection.GeneratedProtocolMessageType('DatasetSummary', (_message.Message,), {

  'ColumnsEntry' : _reflection.GeneratedProtocolMessageType('ColumnsEntry', (_message.Message,), {
    'DESCRIPTOR' : _DATASETSUMMARY_COLUMNSENTRY,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:DatasetSummary.ColumnsEntry)
    })
  ,
  'DESCRIPTOR' : _DATASETSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:DatasetSummary)
  })
_sym_db.RegisterMessage(DatasetSummary)
_sym_db.RegisterMessage(DatasetSummary.ColumnsEntry)

ModelSummary = _reflection.GeneratedProtocolMessageType('ModelSummary', (_message.Message,), {
  'DESCRIPTOR' : _MODELSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:ModelSummary)
  })
_sym_db.RegisterMessage(ModelSummary)

MetricsSummary = _reflection.GeneratedProtocolMessageType('MetricsSummary', (_message.Message,), {
  'DESCRIPTOR' : _METRICSSUMMARY,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:MetricsSummary)
  })
_sym_db.RegisterMessage(MetricsSummary)

ConfusionMatrix = _reflection.GeneratedProtocolMessageType('ConfusionMatrix', (_message.Message,), {
  'DESCRIPTOR' : _CONFUSIONMATRIX,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:ConfusionMatrix)
  })
_sym_db.RegisterMessage(ConfusionMatrix)

ROCCurve = _reflection.GeneratedProtocolMessageType('ROCCurve', (_message.Message,), {
  'DESCRIPTOR' : _ROCCURVE,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:ROCCurve)
  })
_sym_db.RegisterMessage(ROCCurve)

RecallCurve = _reflection.GeneratedProtocolMessageType('RecallCurve', (_message.Message,), {
  'DESCRIPTOR' : _RECALLCURVE,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:RecallCurve)
  })
_sym_db.RegisterMessage(RecallCurve)

DatasetSummaries = _reflection.GeneratedProtocolMessageType('DatasetSummaries', (_message.Message,), {

  'ProfilesEntry' : _reflection.GeneratedProtocolMessageType('ProfilesEntry', (_message.Message,), {
    'DESCRIPTOR' : _DATASETSUMMARIES_PROFILESENTRY,
    '__module__' : 'summaries_pb2'
    # @@protoc_insertion_point(class_scope:DatasetSummaries.ProfilesEntry)
    })
  ,
  'DESCRIPTOR' : _DATASETSUMMARIES,
  '__module__' : 'summaries_pb2'
  # @@protoc_insertion_point(class_scope:DatasetSummaries)
  })
_sym_db.RegisterMessage(DatasetSummaries)
_sym_db.RegisterMessage(DatasetSummaries.ProfilesEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030com.whylogs.core.messageB\tSummariesP\001'
  _CHARPOSSUMMARY_CHARPOSMAPENTRY._options = None
  _CHARPOSSUMMARY_CHARPOSMAPENTRY._serialized_options = b'8\001'
  _SCHEMASUMMARY_TYPECOUNTSENTRY._options = None
  _SCHEMASUMMARY_TYPECOUNTSENTRY._serialized_options = b'8\001'
  _DATASETSUMMARY_COLUMNSENTRY._options = None
  _DATASETSUMMARY_COLUMNSENTRY._serialized_options = b'8\001'
  _DATASETSUMMARIES_PROFILESENTRY._options = None
  _DATASETSUMMARIES_PROFILESENTRY._serialized_options = b'8\001'
  _UNIQUECOUNTSUMMARY._serialized_start=92
  _UNIQUECOUNTSUMMARY._serialized_end=160
  _FREQUENTSTRINGSSUMMARY._serialized_start=162
  _FREQUENTSTRINGSSUMMARY._serialized_end=288
  _FREQUENTSTRINGSSUMMARY_FREQUENTITEM._serialized_start=241
  _FREQUENTSTRINGSSUMMARY_FREQUENTITEM._serialized_end=288
  _FREQUENTNUMBERSSUMMARY._serialized_start=291
  _FREQUENTNUMBERSSUMMARY._serialized_end=569
  _FREQUENTNUMBERSSUMMARY_FREQUENTDOUBLEITEM._serialized_start=435
  _FREQUENTNUMBERSSUMMARY_FREQUENTDOUBLEITEM._serialized_end=502
  _FREQUENTNUMBERSSUMMARY_FREQUENTLONGITEM._serialized_start=504
  _FREQUENTNUMBERSSUMMARY_FREQUENTLONGITEM._serialized_end=569
  _FREQUENTITEMSSUMMARY._serialized_start=571
  _FREQUENTITEMSSUMMARY._serialized_end=698
  _FREQUENTITEMSSUMMARY_FREQUENTITEM._serialized_start=646
  _FREQUENTITEMSSUMMARY_FREQUENTITEM._serialized_end=698
  _CHARPOSSUMMARY._serialized_start=701
  _CHARPOSSUMMARY._serialized_end=863
  _CHARPOSSUMMARY_CHARPOSMAPENTRY._serialized_start=798
  _CHARPOSSUMMARY_CHARPOSMAPENTRY._serialized_end=863
  _STRINGSSUMMARY._serialized_start=866
  _STRINGSSUMMARY._serialized_end=1081
  _SCHEMASUMMARY._serialized_start=1084
  _SCHEMASUMMARY._serialized_end=1241
  _SCHEMASUMMARY_TYPECOUNTSENTRY._serialized_start=1192
  _SCHEMASUMMARY_TYPECOUNTSENTRY._serialized_end=1241
  _HISTOGRAMSUMMARY._serialized_start=1244
  _HISTOGRAMSUMMARY._serialized_end=1372
  _QUANTILESUMMARY._serialized_start=1374
  _QUANTILESUMMARY._serialized_end=1435
  _NUMBERSUMMARY._serialized_start=1438
  _NUMBERSUMMARY._serialized_end=1714
  _COLUMNSUMMARY._serialized_start=1717
  _COLUMNSUMMARY._serialized_end=1964
  _DATASETSUMMARY._serialized_start=1967
  _DATASETSUMMARY._serialized_end=2164
  _DATASETSUMMARY_COLUMNSENTRY._serialized_start=2102
  _DATASETSUMMARY_COLUMNSENTRY._serialized_end=2164
  _MODELSUMMARY._serialized_start=2166
  _MODELSUMMARY._serialized_end=2214
  _METRICSSUMMARY._serialized_start=2217
  _METRICSSUMMARY._serialized_end=2376
  _CONFUSIONMATRIX._serialized_start=2379
  _CONFUSIONMATRIX._serialized_end=2526
  _ROCCURVE._serialized_start=2528
  _ROCCURVE._serialized_end=2582
  _RECALLCURVE._serialized_start=2584
  _RECALLCURVE._serialized_end=2641
  _DATASETSUMMARIES._serialized_start=2644
  _DATASETSUMMARIES._serialized_end=2779
  _DATASETSUMMARIES_PROFILESENTRY._serialized_start=2715
  _DATASETSUMMARIES_PROFILESENTRY._serialized_end=2779
# @@protoc_insertion_point(module_scope)
