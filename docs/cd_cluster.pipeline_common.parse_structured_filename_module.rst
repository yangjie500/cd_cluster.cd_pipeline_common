.. _cd_cluster.pipeline_common.parse_structured_filename_module:


****************************************************
cd_cluster.pipeline_common.parse_structured_filename
****************************************************

**Extract structured key-value metadata from a delimited filename.**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Takes a filename or path, removes common file extensions (including multi-part extensions such as ``.tar.gz``), splits the remaining base filename using a user-defined delimiter, and maps the extracted fields into user-defined field names.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delimiter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Delimiter used to separate metadata fields.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>field_names</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Ordered list of field names used to map extracted values.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filename</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Full filename or path containing structured metadata.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Extract metadata from structured filename
      cd_cluster.pipeline_common.parse_structured_filename:
        filename: "hello+--12345+--v1.1.1+--20052026T121212.tar.gz"
        delimiter: "+--"
        field_names:
          - name
          - tag
          - version
          - datetime
      register: artifact_metadata

    - name: Extract metadata from absolute path
      cd_cluster.pipeline_common.parse_structured_filename:
        filename: "/var/tmp/builds/hello+--12345+--v1.1.1+--20052026T121212.tar.gz"
        delimiter: "+--"
        field_names:
          - name
          - tag
          - version
          - datetime



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>cleaned_base_name</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Filename after extension stripping.</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>extracted_fields</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Ordered list of extracted values.</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>parsed_data</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>Dictionary containing parsed structured metadata.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;name&#x27;: &#x27;hello&#x27;, &#x27;tag&#x27;: &#x27;12345&#x27;, &#x27;version&#x27;: &#x27;v1.1.1&#x27;, &#x27;datetime&#x27;: &#x27;20052026T121212&#x27;}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Yang Jie (@yangjie500)
